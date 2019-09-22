## Googleアカウントの認証を使って、JWTを取得
* ログイン用のURL（Domain）の設定
    * https://ys-dev-web.auth.us-west-2.amazoncognito.com
* Googleの開発アカウントの設定
    * アプリケーションの種類
        * ウェブアプリケーション
    * 認証済みのリダイレクトURI
        * https://ys-dev-web.auth.us-west-2.amazoncognito.com/oauth2/idpresponse
* CognitoでGoogle連携の設定
    * Googleの開発アカウントで取得した、ClientId、ClientSecretを設定する
    * ![cognito-app-settings](../picture/cognito-app-settings.PNG)
* コールバック用のWebアプリ設定
    * ローカルのダミーWebアプリでOK
    * http://locahost
* ログイン用URLにアクセスし、Googleアカウントで認証
    * https://ys-dev-web.auth.us-west-2.amazoncognito.com/login?response_type=code&client_id={clientId}&redirect_uri=http://localhost
    * ![cognito-login](../picture/cognito-login.PNG)
* 上記のコールバックURLについてくる認証コードの取得
    * http://localhost/?code=XXXX
* 上記の認証コードを使って、JWTの取得
    ```
    curl -X POST -H 'Content-Type:application/x-www-form-urlencoded' --verbose 'https://ys-dev-web.auth.us-west-2.amazoncognito.com/oauth2/token?grant_type=authorization_code&client_id=xxxx&redirect_uri=http://localhost&code=xxxx'
    ```
* IdToken(JWT)をAuthorizationヘッダに付与して、ApiGatewayにアクセスする
    * 有効期限内の1時間はこれでOK、切れた場合は更新が必要
* Refresh Tokenを使って、IdTokenを更新
    ```
    curl -X POST -H 'Content-Type:application/x-www-form-urlencoded' --verbose 'https://ys-dev-web.auth.us-west-2.amazoncognito.com/oauth2/token?grant_type=refresh_token&client_id=xxxx&refresh_token=xxxx
    ```
