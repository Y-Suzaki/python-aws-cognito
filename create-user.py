import boto3
import os

ACCOUNT_ID = os.environ['ACCOUNT_ID']
USER_POOL_ID = os.environ['USER_POOL_ID']
USER_ID = "z-suzaki"
PASSWORD = os.environ['PASSWORD']
CLIENT_ID = os.environ['CLIENT_ID']
IDENTITY_POOL_ID = os.environ['IDENTITY_POOL_ID']
TARGET_S3_BUCKET = "ys-dev-web-deploy-module"

region = 'ap-northeast-1'
aws_client = boto3.client('cognito-idp', region_name=region)


def create_user(user_name: str, password: str):
    """ Cognito UserPoolに新規ユーザーの作成 """
    response = aws_client.admin_create_user(
        UserPoolId=USER_POOL_ID,
        Username=user_name,
        TemporaryPassword=password,
        MessageAction='SUPPRESS',   # RESENDにすればメールも送る
    )
    print(response)


def confirm_password(user_name: str, password: str):
    """ パスワードの設定を行う。用途は、NEW_PASSWORD_REQUIREDを強制的に書き換えるため。 """
    response = aws_client.admin_set_user_password(
        UserPoolId=USER_POOL_ID,
        Username=user_name, Password=password,
        Permanent=True)
    print(response)


_user_name = USER_ID
_password = PASSWORD

create_user(_user_name, _password)
confirm_password(_user_name, _password)
