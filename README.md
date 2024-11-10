# xpost-reddit-to-fediverse

An example bot (meant for deployment in Lambda) that cross-posts **direct links** from a given subreddit to up-and-coming federated platforms, helping to seed them with content (without simply linking back to Reddit).

This posts *direct links only*, so for the example post:

* "So, someone tried baiting people into downloading malware on r/cybersecurity (it didn't work) - a brief writeup" posted to r/cybersecurity at https://www.reddit.com/r/cybersecurity/comments/16wqej3/so_someone_tried_baiting_people_into_downloading/
* The title of the post and *destination linked by the post* (https://chris.partridge.tech/2023/malware-targeting-cybersecurity-subreddit/) would be posted on federated social media

Currently, this bot is used to cross-post links:

* From r/netsec
  * to Mastodon at [@netsec@botsin.space](https://botsin.space/@netsec)
  * to Bluesky at [@r-netsec.bsky.social](https://bsky.app/profile/r-netsec.bsky.social)
* From r/blueteamsec
  * to Bluesky at [@r-blueteamsec.bsky.social](https://bsky.app/profile/r-blueteamsec.bsky.social)

### Moderation

To limit the chance that spam or other unwanted content is cross-posted by this bot, some useful features are on and enabled by default:

* **Time delay:** This bot includes a short delay before new posts are eligible for cross-posting so the Reddit community's automated tools (such as AutoModerator) are ~guaranteed to have run. This also increases the chance that any unwanted content has been reported and removed by the subreddit's moderators and Reddit administration, but does not guarantee it (ex. subreddit moderators are volunteers, and may be offline).
* **Vote count and ratio filter:** This bot can be configured to require a certain number of upvotes or a certain post ratio before posting. This can help avoid irrelevant content that was posted by non-community-members, as well as intentional spam. While this can be bypassed with bought votes, that increases the chance the content is removed by Reddit administration.
* **DNS filtering:** This bot also includes a DNS-based filtering mechanism to limit what links are posted, and is set by default to prevent posting any known-NSFW (e.g. pornography) sites. You can use a DNS filter of your choice, ex. NextDNS, to pare down what sites can be posted (I recommend doing this so you can also filter new domains). If DNS filtering is not wanted, you can disable filtering by placing a non-filtering DNS resolver ex. Google DNS instead (this will instead ensure the link contains a valid and resolvable domain - so it's still a value add).

However, the bot is not "smart" and does not have other features to limit unwanted content. If it sees links that pass the above checks, it *will* post them. *Therefore this bot should only be used on active, well-moderated subreddits.*

If you are 'hunting for an occasional gem' on a subreddit, just post links that interest you manually, don't use a bot!

### Limitations

Because the bot is focused only on posting direct links, it will *only* work for subreddits which are primarily used as link aggregators.