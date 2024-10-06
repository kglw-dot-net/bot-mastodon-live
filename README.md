# bot-mastodon-live

🚧 🏗️ Work In Progress 🔧 👷

This is a Mastodon bot, which uses the [KGLW.net] [API](https://kglw.net/api/docs.php) to identify the latest setlist and then posts the song title of the last song in the setlist.

If a [KGLW.net] Staff Member is updating the setlist in realtime (*this is an assumption*), this bot will be posting each song title "as soon as" it's identified!


## Docs

* [Mastodon.py](https://mastodonpy.readthedocs.io/en/stable/index.html)


## Ops

This bot runs via AWS Lambda, on [Axe](https://forum.kglw.net/u/supremeaxendancy/summary)'s personal account.

It is triggered by a webhook set up in the Songfish back-end, which fires whenever a setlist is edited.

[KGLW.net]: https://kglw.net
