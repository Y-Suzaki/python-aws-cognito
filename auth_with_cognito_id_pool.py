import boto3
import os
from boto3.session import Session
import requests
from requests_aws4auth import AWS4Auth

ACCOUNT_ID = os.environ['ACCOUNT_ID']
USER_POOL_ID = os.environ['USER_POOL_ID']
USER_ID = "y-suzaki"
PASSWORD = os.environ['PASSWORD']
CLIENT_ID = os.environ['CLIENT_ID']
IDENTITY_POOL_ID = os.environ['IDENTITY_POOL_ID']
TARGET_S3_BUCKET = "ys-dev-web-deploy-module"
API_URL = os.environ['API_URL']

region = 'ap-northeast-1'


def auth(user_id, password):
    """Cognito認証（Cognito UserPool）"""
    aws_client = boto3.client('cognito-idp', region_name=region)
    auth_result = aws_client.admin_initiate_auth(
        UserPoolId=USER_POOL_ID,
        ClientId=CLIENT_ID,
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters={
            "USERNAME": user_id,
            "PASSWORD": password,
        }
    )
    return auth_result


def authorize(id_token):
    """認可"""
    aws_client = boto3.client('cognito-identity', region_name=region)
    logins = {f'cognito-idp.{region}.amazonaws.com/{USER_POOL_ID}': id_token}

    cognito_identity_id = aws_client.get_id(
        AccountId=ACCOUNT_ID,
        IdentityPoolId=IDENTITY_POOL_ID,
        Logins=logins
    )

    credentials = aws_client.get_credentials_for_identity(
        IdentityId=cognito_identity_id['IdentityId'],
        Logins=logins
    )
    return credentials['Credentials']


def list_on_s3(credential):
    """Bucket内のオブジェクト一覧"""
    session = Session(
        aws_access_key_id=credential['AccessKeyId'],
        aws_secret_access_key=credential['SecretKey'],
        aws_session_token=credential['SessionToken'])

    s3_resource = session.resource('s3')
    bucket = s3_resource.Bucket(TARGET_S3_BUCKET)
    for key in bucket.objects.all():
        print(key.key)


def access_api_gateway(credential):
    """ IAM認証されたAPIGatewayにアクセスする。 """
    aws_auth = AWS4Auth(
        credential['AccessKeyId'],
        credential['SecretKey'],
        region,
        'execute-api',
        session_token=credential['SessionToken'],
    )
    response = requests.get(API_URL, auth=aws_auth)
    print(response.text)


_auth_result = auth(USER_ID, PASSWORD)
_credential = authorize(id_token=_auth_result["AuthenticationResult"]["IdToken"])
list_on_s3(_credential)
access_api_gateway(_credential)

print('Completed!')
