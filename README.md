# Bring Link Aggregator Subreddits to the Fediverse

[![License](https://img.shields.io/github/license/tweedge/xpost-reddit-to-fediverse)](https://github.com/tweedge/xpost-reddit-to-fediverse)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

An example bot (meant for deployment in Lambda) that cross-posts **direct links** from a given subreddit to up-and-coming federated platforms, helping to seed them with content without simply linking back to Reddit.

This posts *direct links only*, so for the example post:

* "So, someone tried baiting people into downloading malware on r/cybersecurity (it didn't work) - a brief writeup" posted to r/cybersecurity at https://www.reddit.com/r/cybersecurity/comments/16wqej3/so_someone_tried_baiting_people_into_downloading/
* The title of the post and *destination linked by the post* (https://chris.partridge.tech/2023/malware-targeting-cybersecurity-subreddit/) would be posted on federated social media

### Used By

I use this bot to cross-post my favorite link aggregator subreddits to the social media sites where I now spend my time:

* From r/netsec
  * to Mastodon at [@netsec@botsin.space](https://botsin.space/@netsec)
  * to Bluesky at [@r-netsec.bsky.social](https://bsky.app/profile/r-netsec.bsky.social)
* From r/blueteamsec
  * to Bluesky at [@r-blueteamsec.bsky.social](https://bsky.app/profile/r-blueteamsec.bsky.social)
* From r/redteamsec
  * to Bluesky at [@r-redteamsec.bsky.social](https://bsky.app/profile/r-redteamsec.bsky.social)

### Moderation

To limit the chance that spam or other unwanted content is cross-posted by this bot, some useful features are on and enabled by default:

* **Time delay:** This bot includes a short delay before new posts are eligible for cross-posting so the Reddit community's automated tools (such as AutoModerator) are ~guaranteed to have run. This also increases the chance that any unwanted content has been reported and removed by the subreddit's moderators and Reddit administration, but does not guarantee it (ex. subreddit moderators are volunteers, and may be offline).
* **Vote count and ratio filter:** This bot can be configured to require a certain number of upvotes or a certain post ratio before posting. This can help avoid irrelevant content that was posted by non-community-members, as well as intentional spam. While this can be bypassed with bought votes, that increases the chance the content is removed by Reddit administration.
* **DNS filtering:** This bot also includes a DNS-based filtering mechanism to limit what links are posted, and is set by default to prevent posting any known-NSFW (e.g. pornography) sites. You can use a DNS filter of your choice, ex. NextDNS, to pare down what sites can be posted (I recommend doing this so you can also filter new domains). If DNS filtering is not wanted, you can disable filtering by placing a non-filtering DNS resolver ex. Google DNS instead (this will instead ensure the link contains a valid and resolvable domain - so it's still a value add).

However, the bot is not "smart" and does not have other features to limit unwanted content. If it sees links that pass the above checks, it *will* post them. *Therefore this bot should only be used on active, well-moderated subreddits.*

If you are 'hunting for an occasional gem' on a subreddit, just post links that interest you manually, don't use a bot!

### Considerations

Because the bot only posts direct links and doesn't have readers go through Reddit as an interstitial/doesn't link to the comment section, it will *only* work for subreddits which are primarily used as **link aggregators.**

The decisions made in this bot are generally good for people who may object to using Reddit directly but find value in the communities that have formed on Reddit, or are moving away from Reddit gradually, etc.

I also wrote a bot oriented towards discussion-focused subreddits, the ["Best Of" r/cybersecurity bot](https://github.com/r-cybersecurity/best-of-bot), which summarizes posts and links to Reddit so people can read the full discussion including comments.