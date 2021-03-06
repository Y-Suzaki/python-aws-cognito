import boto3
from boto3.session import Session

ACCOUNT_ID = "838023436798"
USER_POOL_ID = "us-west-2_QsC6VTvKW"
USER_ID = "test@gmail.com"
PASSWORD = "tanyao30"
CLIENT_ID = "3c67mu2rbgpmco90vmcv7pk7ui"
IDENTITY_POOL_ID = "us-west-2:5383de4b-f345-4189-b0ab-cae5c62c68a3"
TARGET_S3_BUCKET = "ys-dev-web-iot-rule-test"


def auth(user_id, password):
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


def authorize(id_token):
    """認可"""
    aws_client = boto3.client('cognito-identity', region_name='us-west-2')
    logins = {'cognito-idp.us-west-2.amazonaws.com/' + USER_POOL_ID: id_token}

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


auth_result = auth(USER_ID, PASSWORD)
credential = authorize(id_token=auth_result["AuthenticationResult"]["IdToken"])
list_on_s3(credential)

print('Completed!')
