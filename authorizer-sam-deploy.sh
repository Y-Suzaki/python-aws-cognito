#!/bin/bash -e

s3_bucket="cf-templates-461spye58s2i-us-west-2"

echo "** Start to deploy and build. **"
mkdir -p deploy
pip3 install requests -t deploy
pip3 install python-jose -t deploy
cp authorizer.py deploy
cd deploy
zip -r ../serverless-function.zip *
cd ..

echo "Package serverless function..."
aws cloudformation package \
  --template-file authorizer-sam.yaml \
  --output-template-file aws-sam-deploy.yaml \
  --s3-bucket ${s3_bucket} \
  --s3-prefix serverless-function \
  --region us-west-2 \
  --profile default

echo "Deploy serverless function..."
aws cloudformation deploy \
  --template-file aws-sam-deploy.yaml \
  --stack-name serverless-function \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides ArtifactBucket=${s3_bucket} \
  --region us-west-2 \
  --profile default

echo "** All complete! **"
aws s3 rm s3://${s3_bucket}/serverless-function/ \
  --region us-west-2 \
  --profile default \
  --recursive

rm -rf deploy
rm -f aws-sam-deploy.yaml serverless-function.zip
