import os
from datetime import datetime
from mastodon import Mastodon

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

mastodon = Mastodon(access_token=ACCESS_TOKEN, api_base_url='https://botsin.space/')

def lambda_handler(event, context):
    mastodon.status_post(f'hello world! {datetime.now()}')
