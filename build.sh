#!/bin/bash

# cleanup
rm -rf deploy_me.zip package

# install Lambda-compatible version of cryptography
pip install \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python 3.10 \
    --only-binary=:all: --upgrade \
    --target ./package \
    "cryptography<42"

# install dependencies
pip3 install --target ./package "urllib3<2" Mastodon.py atproto==0.0.34 dns-mollusc praw

# build zip with all data
cd package
zip -r ../deploy_me.zip .
cd ..
zip -g deploy_me.zip lambda_function.py