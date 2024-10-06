import os
from mastodon import Mastodon
import json
from urllib.request import urlopen, Request

mastodon = Mastodon(access_token=os.getenv('ACCESS_TOKEN'), api_base_url='https://botsin.space/')

def kglw_api_fetch_json(url):
    return json.loads(
            urlopen(Request(
                url,
                headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
                )).read())

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    if 'show_id' not in payload:
        raise Exception(f'payload does not look correct, expected body with json-formatted payload: {payload}')
    latest_json = kglw_api_fetch_json('http://kglw.net/api/v2/latest.json')
    if latest_json['data'][0]['show_id'] != payload['show_id']:
        raise Exception(f'webhook fired for show_id:{payload['show_id']} but that is not the most recent show ({latest_json['data'][0]['show_id']})')
    last_song = latest_json['data'][-1] # TODO subtle bug: if they start a show with the same song which ended the show prior, the show-starting song won't be posted...
    last_toot = mastodon.account_statuses(mastodon.me()['id'])
    if last_toot['content'] == f'<p>{last_song['songname']}</p>':
        raise Exception('we already tooted about this song...', json.dumps(last_toot), json.dumps(last_song))
    try:
        # TODO: reply to last toot from current show... mastodon.status_reply(last_toot, last_song['songname'])
        return json.dumps(mastodon.status_post(last_toot, last_song['songname']), default=str)
    except Exception as err:
        print(err)
        return json.dumps({'status':'something borked', 'error':err, 'toot':toot}, default=str)
