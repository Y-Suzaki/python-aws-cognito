import boto3
from boto3.session import Session

ACCOUNT_ID = ""
FACEBOOK_TEST_TOKEN = ""
CLIENT_ID = ""
IDENTITY_POOL_ID = ""
TARGET_S3_BUCKET = ""


def auth():
    """FaceBook認証"""
    # 実際はjsとかでFaceBookのログインを促し、AccessTokenを取得する必要がある。
    return FACEBOOK_TEST_TOKEN


def authorize(id_token):
    """認可"""
    aws_client = boto3.client('cognito-identity', region_name='us-west-2')
    logins = {'graph.facebook.com': id_token}

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


id_token = auth()
credential = authorize(id_token=id_token)
list_on_s3(credential)

print('Completed!')
