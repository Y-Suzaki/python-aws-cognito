### AWS CLIでCognitoユーザーのパスワード変更
```$xslt
aws cognito-idp admin-initiate-auth \
--user-pool-id us-west-2_xxxx \
--client-id xxxx \
--auth-flow ADMIN_NO_SRP_AUTH \
--auth-parameters \
USERNAME=xxxx,PASSWORD=xxxx
  -> sessionが取得できる 

aws cognito-idp admin-respond-to-auth-challenge \
--user-pool-id us-west-2_xxxx \
--client-id xxxx \
--challenge-name NEW_PASSWORD_REQUIRED \
--challenge-responses NEW_PASSWORD='xxxx',USERNAME=xxxx \
--session "xxx"
```