import boto3
import json
import os
import requests
import time
from urllib.parse import urlparse
from atproto import Client
from atproto.xrpc_client.models import AppBskyEmbedExternal
from html import unescape
from botocore.exceptions import ClientError, NoCredentialsError
from mastodon import Mastodon
from dns_mollusc import mollusc_client


client = boto3.client("dynamodb")
# create domain filter, because spammers on Reddit are that bad
if os.getenv("DNS_FILTER"):  # filter whatever you want
    dns_client = mollusc_client(os.getenv("DNS_FILTER"), 20)
else:  # otherwise, baseline at "bot must be SFW" by default
    dns_client = mollusc_client("https://family.cloudflare-dns.com/dns-query?", 20)


def lambda_handler(event, context):
    subreddit = os.getenv("SUBREDDIT")
    url = f"https://www.reddit.com/r/{subreddit}/new/.json?count=25"
    headers = {"User-Agent": "r/cybersecurity Beyond"}

    try:
        fetched_data = requests.get(url, headers=headers)
    except Exception:
        return {"statusCode": 500, "body": "Couldn't GET Reddit"}

    try:
        json_data = fetched_data.json()
    except Exception:
        return {"statusCode": 500, "body": "Reddit did not return valid JSON"}

    if "data" not in json_data:
        return {"statusCode": 500, "body": "JSON does not contain 'data' field."}

    try:
        posts_raw = json_data["data"]["children"]
    except Exception as e:
        return {"statusCode": 500, "body": f"JSON may be malformed due to {e}"}

    posts_clean = []
    for post_raw in posts_raw:
        post = post_raw["data"]

        post_title = post["title"]
        post_url = post["url"]
        post_created_epoch = post["created"]
        ddb_key = f"{subreddit}->{post_url}"

        if post_url.startswith("https://www.reddit.com"):
            continue

        if time.time() < post_created_epoch + (15 * 60):
            # post is less than 15m old, strongly increases chance that the post
            # is unmoderated, for ex. AutoMod may not run for 0-3m in typical use
            continue

        posts_clean.append({"title": post_title, "url": post_url, "key": ddb_key})

    posted = False
    for post in posts_clean:
        if posted:
            break

        # check in DynamoDB if we've attempted posting this yet
        dynamo_get = []
        try:
            dynamo_get = client.get_item(
                TableName="BeyondState",
                Key={"dedupe": {"S": post["key"]}},
            )
        except ClientError as e:
            print(f"-- DynamoDB GET failed: {e.response['Error']['Message']}")
            # we don't know if we've posted this, so let's skip it
            # this enforces at most once posting
            continue
        except NoCredentialsError:
            # local devel without access to DDB, just keep going
            pass

        # we've already seen this submission, skip it
        if "Item" in dynamo_get:
            print("-- already known, skipping")
            continue

        # we haven't posted the submission, try logging that we intend to post it
        expires = str((60 * 24 * 60 * 60) + int(time.time()))  # 60 days from now
        try:
            client.put_item(
                TableName="BeyondState",
                Item={"dedupe": {"S": post["key"]}, "ttl": {"N": expires}},
            )
        except ClientError as e:
            print(f"-- DynamoDB PUT failed: {e.response['Error']['Message']}")
            # we don't know if we've saved this, so let's skip it
            # this enforces at most once posting
            continue
        except NoCredentialsError:
            # local devel without access to DDB, just keep going
            pass
        except Exception as e:
            print(e)
            # we don't know if we've saved this, so let's skip it
            # this enforces at most once posting
            continue

        # we're checking the domain this late because if we don't want to post
        # that should be logged and prevent future post/lookup attempts
        domain = urlparse(post["url"]).netloc
        filter_result = client.query(domain)
        if filter_result.is_blocked_by_server():
            print(f"-- {domain} is filtered by resolver, skipping")
            continue

        print("-- good to go, posting!")
        title = unescape(post["title"])
        post_toot(title, post["url"])
        post_skeet(title, post["url"])
        posted = True

    if posted:
        return {"statusCode": 200, "body": "Posted successfully."}
    if not posted:
        return {"statusCode": 200, "body": "Exhausted all options for posting."}


def clean_tokens(text_data):
    tokens_to_clean = text_data.split(" ")

    clean_tokens = []
    for token_to_clean in tokens_to_clean:
        # could also ensure no cashtags?
        clean_token = token_to_clean.strip("#@")
        clean_tokens.append(clean_token)

    return " ".join(clean_tokens)


def post_toot(title, link):
    print("-- attempting toot")
    post_me = f"{title} {link}"

    try:
        MASTO_CLIENT_KEY = os.getenv("MASTO_CLIENT_KEY")
        MASTO_CLIENT_SECRET = os.getenv("MASTO_CLIENT_SECRET")
        MASTO_ACCESS_TOKEN = os.getenv("MASTO_ACCESS_TOKEN")

        if MASTO_CLIENT_KEY and MASTO_CLIENT_SECRET and MASTO_ACCESS_TOKEN:
            mastodon = Mastodon(
                api_base_url="https://botsin.space",
                client_id=MASTO_CLIENT_KEY,
                client_secret=MASTO_CLIENT_SECRET,
                access_token=MASTO_ACCESS_TOKEN,
            )
            mastodon.toot(post_me)
            print(f"-- tooted {post_me}")
            return True
        else:
            print("-- environment variables not present to toot")
    except Exception as e:
        print(f"-- toot caused exception {str(e)}")
        return False


def post_skeet(title, link):
    print("-- attempting skeet")

    try:
        BSKY_USERNAME = os.getenv("BSKY_USERNAME")
        BSKY_PASSWORD = os.getenv("BSKY_PASSWORD")

        if BSKY_USERNAME and BSKY_PASSWORD:
            client = Client()
            client.login(BSKY_USERNAME, BSKY_PASSWORD)
            external_link = AppBskyEmbedExternal.External(
                uri=link, description="", title=title
            )
            client.send_post(
                text=title, embed=AppBskyEmbedExternal.Main(external=external_link)
            )
            print(f"-- skeeted {title}")
            return True
        else:
            print("-- environment variables not present to skeet")
    except Exception as e:
        print(f"-- skeet caused exception {str(e)}")
        return False


if __name__ == "__main__":
    print(lambda_handler({}, {}))
