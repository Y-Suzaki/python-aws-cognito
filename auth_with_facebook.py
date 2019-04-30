import boto3
from boto3.session import Session

ACCOUNT_ID = "838023436798"
FACEBOOK_TEST_TOKEN = "EAAFgsUKZBw08BAEVZC0ZCUIOVbKlSVuD0ahXIIeLTNigfqnFkYiMK3zMcqKlTP8vMKqDIomaZBwugpIuZBj64EZC5hrZBdcZAD50Phw3ryDZCEZClOuD6CH4ZABfqYjZAwI8EkcD5H1F1C8gytzITJuWNgPoer6ZA1Nlm3QMu0xF4yaZBpkjQJCqXkLhguhrcwrGX68GYZD"
CLIENT_ID = "3c67mu2rbgpmco90vmcv7pk7ui"
IDENTITY_POOL_ID = "us-west-2:5383de4b-f345-4189-b0ab-cae5c62c68a3"
TARGET_S3_BUCKET = "ys-dev-web-iot-rule-test"


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
