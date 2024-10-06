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
    # print(event) # {'version': '2.0', 'routeKey': '$default', 'rawPath': '/', 'rawQueryString': '', 'headers': {'x-amzn-tls-cipher-suite': 'TLS_AES_128_GCM_SHA256', 'content-length': '22', 'x-amzn-tls-version': 'TLSv1.3', 'x-amzn-trace-id': 'Root=1-6702f6d6-3fb160a70097001a5e0a4e0c', 'x-forwarded-proto': 'https', 'host': 'nt5stl52n2onybi5jumuj6tadi0zneub.lambda-url.us-west-1.on.aws', 'x-forwarded-port': '443', 'content-type': 'application/json', 'x-forwarded-for': '149.28.253.24', 'accept': '*/*'}, 'requestContext': {'accountId': 'anonymous', 'apiId': 'nt5stl52n2onybi5jumuj6tadi0zneub', 'domainName': 'nt5stl52n2onybi5jumuj6tadi0zneub.lambda-url.us-west-1.on.aws', 'domainPrefix': 'nt5stl52n2onybi5jumuj6tadi0zneub', 'http': {'method': 'POST', 'path': '/', 'protocol': 'HTTP/1.1', 'sourceIp': '149.28.253.24', 'userAgent': None}, 'requestId': '48f8234a-3f06-4c1e-9064-e79c0c7253c7', 'routeKey': '$default', 'stage': '$default', 'time': '06/Oct/2024:20:45:10 +0000', 'timeEpoch': 1728247510542}, 'body': '{"show_id":1685718366}', 'isBase64Encoded': False}
    # print(context) # LambdaContext([aws_request_id=48f8234a-3f06-4c1e-9064-e79c0c7253c7,log_group_name=/aws/lambda/kglwBotMastodonLive,log_stream_name=2024/10/06/[$LATEST]059dd134fb954520b85825bc34424ab3,function_name=kglwBotMastodonLive,memory_limit_in_mb=128,function_version=$LATEST,invoked_function_arn=arn:aws:lambda:us-west-1:110643462061:function:kglwBotMastodonLive,client_context=None,identity=CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])])

    payload = json.loads(event['body'])

    if 'show_id' not in payload:
        raise Exception(f'payload does not look correct, expected body with json-formatted payload: {payload}')

    latest_json = kglw_api_fetch_json('http://kglw.net/api/v2/latest.json')
    print(f'latest show... {latest_json}')

    if latest_json['data'][0]['show_id'] != payload['show_id']:
        raise Exception(f'webhook fired for show_id:{payload['show_id']} but that is not the most recent show ({latest_json['data'][0]['show_id']})')

    last_song = latest_json['data'][-1]
    print(last_song['songname'])

    last_toot = mastodon.account_statuses(mastodon.me()['id'])
    if last_toot['content'] == f'<p>{last_song['songname']}</p>':
        raise Exception('we already tooted about this song...', json.dumps(last_toot), json.dumps(last_song))

    try:
        # TODO: reply to last toot from current show... mastodon.status_reply(last_toot, last_song['songname'])
        return json.dumps(mastodon.status_post(last_toot, last_song['songname']), default=str)
    except Exception as err:
        print(err)
        return json.dumps({'status':'something borked', 'error':err, 'toot':toot}, default=str)
