#!/bin/bash
set -euxo pipefail

# h/t https://matduggan.com/make-a-mastodon-bot-on-aws-free-tier/

test -d package && rm -r package
mkdir package
cp lambda_function.py package
python -m venv venv
source venv/bin/activate
pip install --target ./package datetime
pip install --target ./package Mastodon.py
# need to zip the working directory so that Lambda finds the lambda_function.py file...
cd package && zip -r ../package.zip . && cd -

# env vars are configured in the lambda UX
