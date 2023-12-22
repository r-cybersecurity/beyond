#!/bin/bash

# cleanup
rm -rf deploy_me.zip package

# install dependencies
pip3 install --target ./package "urllib3<2" requests Mastodon.py atproto==0.0.34 dns-mollusc

# build zip with all data
cd package
zip -r ../deploy_me.zip .
cd ..
zip -g deploy_me.zip lambda_function.py