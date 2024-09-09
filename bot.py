from mastodon import Mastodon

mastodon = Mastodon(
    access_token = 'token.secret', # this is a file containing the account's Access Token
    api_base_url = 'https://botsin.space/')

mastodon.status_post("hello world!")
