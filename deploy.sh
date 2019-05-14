#!/bin/bash

aws cloudformation deploy \
    --template-file configurations/udacity.template.yaml \
    --stack-name udacity \
    --capabilities CAPABILITY_NAMED_IAM