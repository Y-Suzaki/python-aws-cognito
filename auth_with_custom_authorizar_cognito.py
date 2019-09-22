import boto3
import requests
from boto3.session import Session

#
# カスタムオーソライザーを設定したApiGatewayにアクセスするサンプル
# オーソライザーのタイプはCognitoを使用する
# 認証プロバイダとしては、CognitoUserPoolとGoogleで試した。
#

ACCOUNT_ID = "838023436798"
USER_POOL_ID = "us-west-2_HV5bF30H6"
USER_ID = "geranium04.24.1981@gmail.com"
PASSWORD = "tanyao30"
CLIENT_ID = "5f55sk2msbsg1t2mi2q2vmvk1e"
API_URL = "https://i02n1l6252.execute-api.us-west-2.amazonaws.com/prod/cognito"


def auth_with_user_pool(user_id: str, password: str):
    """Cognito認証（Cognito UserPool）"""
    aws_client = boto3.client('cognito-idp', region_name='us-west-2')
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


def api(id_token: str):
    # Authorization Headerを正しく設定しないと、401（Unauthorized）になる
    headers = {'Authorization': id_token, 'User-Agent': 'cognito-authorizer'}

    """IdTokenを設定し、ApiGatewayにアクセスする"""
    response = requests.get(API_URL, headers=headers)

    return response


# Cognito認証を使った場合
auth_result = auth_with_user_pool(USER_ID, PASSWORD)
response = api(auth_result["AuthenticationResult"]["IdToken"])
print('**** Cognito ****')
print(response)
print(response.json())

# Google認証を使った場合（事前にJWTの取得をしていることを前提にしている）
# id_token = ''
# response = api(id_token)
# print('**** Google ****')
# print(response)
# print(response.json())

