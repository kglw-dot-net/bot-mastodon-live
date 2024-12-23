#!/bin/bash
set -euxo pipefail

# h/t https://matduggan.com/make-a-mastodon-bot-on-aws-free-tier/

test -d package && rm -r package
mkdir package

cp lambda_function.py package

python -m venv venv
source venv/bin/activate
pip freeze > reqs.txt
pip install --requirement reqs.txt --target ./package
# pip install --target ./package urllib3
# pip install --target ./package json # NB not working...
# pip install --target ./package Mastodon.py

# need to zip the working directory so that Lambda finds the lambda_function.py file...
cd package && zip -r ../package.zip . && cd -

# env vars are configured in the lambda UX
