#!/usr/bin/env bash

rm lambda.zip
echo "Zipping"
zip -q -r lambda.zip -@ < zip_files.txt
echo "Uploading"
aws lambda update-function-code --profile personal --zip-file fileb://lambda.zip --function-name AlexaToHome