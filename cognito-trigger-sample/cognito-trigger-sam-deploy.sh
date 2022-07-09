#!/bin/bash -e

s3_bucket="ys-dev-web-deploy-module"

echo "** Start to deploy and build. **"
mkdir -p deploy
#pip3 install requests -t deploy
#pip3 install python-jose -t deploy
cp trigger.py deploy
cd deploy
zip -r ../serverless-function.zip *
cd ..

echo "Package serverless function..."
aws cloudformation package \
  --template-file cognito-trigger-sam.yml \
  --output-template-file aws-sam-deploy.yml \
  --s3-bucket ${s3_bucket} \
  --s3-prefix cognito-trigger \
  --region ap-northeast-1 \
  --profile default

echo "Deploy serverless function..."
aws cloudformation deploy \
  --template-file aws-sam-deploy.yml \
  --stack-name cognito-trigger-serverless-function \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --profile default

echo "** All complete! **"
aws s3 rm s3://${s3_bucket}/cognito-trigger/ \
  --region ap-northeast-1 \
  --profile default \
  --recursive

rm -rf deploy
rm -f aws-sam-deploy.yaml serverless-function.zip
