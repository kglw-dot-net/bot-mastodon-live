# bot-mastodon-live

This is a Mastodon bot, which uses the [KGLW.net] [API](https://kglw.net/api/docs.php) to identify the latest setlist and then posts the song title of the last song in the setlist.

If a [KGLW.net] Staff Member is updating the setlist in realtime (*this is an assumption*), this bot will be posting each song title "as soon as" it's identified!


## TODO

* [ ] move account to new server https://mastodon.social/@kinggizzbot
* [ ] tests
* [ ] types
* [ ] automatic day-of-show / "doors time" post, with venue name & link to kglw.net setlist (mark the start of the show )
  * [ ] add subsequent song-title posts as responses to this/these posts


## Docs

* [Mastodon.py](https://mastodonpy.readthedocs.io/en/stable/index.html)


## Ops

This bot runs via AWS Lambda, on [Axe](https://forum.kglw.net/u/supremeaxendancy/summary)'s personal account.

It is triggered by a webhook set up in the Songfish back-end, which fires whenever a setlist is edited.

The important part of the webhook payload looks like this:

```json
{
  "body": "{ \"show_id\": 1694538236 }"
}
```

...but the actual payload includes more AWS-y stuff.


### Setup

1. Create new Lambda Function...
  * pick a name like "kglwBotMastodonLive"
  * using Python (3.12 at time of writing)
  * check-on "Enable function URL" ("Use function URLs to assign HTTP(S) endpoints to your Lambda function") ... once you've created this function, the "function URL" will be something like `https://HASH_HERE.lambda-url.us-west-1.on.aws/`
  * Auth type: `NONE` — "Lambda won't perform IAM authentication on requests to your function URL. The URL endpoint will be public unless you implement your own authorization logic in your function"
    * TODO this is an area for improvement...
  * other options left to default…
    * arch: x86_64
    * execution role: "Create a new role with basic Lambda permissions" ("Lambda will create an execution role … with permission to upload logs to Amazon CloudWatch Logs")
    * Invoke mode: BUFFERED
2. set env vars so the Lambda Function sees 'em...

[KGLW.net]: https://kglw.net
