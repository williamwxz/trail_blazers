#!/bin/bash

aws cloudformation update-stack \
    --template-body configurations/udacity.template.yaml \
    --stack-name udacity \
    --capabilities CAPABILITY_NAMED_IAM