import os
from mastodon import Mastodon
import json
from urllib.request import urlopen, Request

mastodon = Mastodon(access_token=os.getenv('ACCESS_TOKEN'),
                    api_base_url='https://botsin.space/')

def kglw_api_fetch_json(url):
    return json.loads(
            urlopen(Request(
                url,
                headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
                )).read())

def lambda_handler(event, _context):
    payload = json.loads(event['body'])
    print('payload', payload)
    if 'show_id' not in payload:
        print('show_id not in payload...')
        raise Exception(f'payload does not look correct, expected body with json-formatted payload: {payload}')
    id_show_just_edited = payload['show_id']
    latest_json = kglw_api_fetch_json('http://kglw.net/api/v2/latest.json')['data']
    last_song = latest_json[-1]
    if last_song['show_id'] != id_show_just_edited:
        print(f'webhook fired for show_id:{id_show_just_edited} but that is not the most recent show ({last_song['show_id']})')
        raise Exception(f'webhook fired for show_id:{id_show_just_edited} but that is not the most recent show ({last_song['show_id']})')
    print('last_song', last_song)
    print(f'gonna try to post a new toot about {last_song['songname']} (idempotency_key=show_id:{id_show_just_edited}/song_id:{last_song['uniqueid']})')
    try:
        post_result = mastodon.status_post(
                last_song['songname'],
                idempotency_key=f'show_id:{id_show_just_edited}/song_id:{last_song['uniqueid']}'
                )
        return json.dumps(post_result, default=str)
    except Exception as err:
        print('error...', err)
        return json.dumps({'status':'something borked', 'error':err, 'toot':toot}, default=str)
