# 笑顔判定ボット

## このアプリの目的

LINE から人物が写った画像を送ることにより、その表情から感情分析した結果を BOT として返します。
AWS Rekognition を使った画像処理を体験する事ができます。
体験することが目的のため仕様は簡単にしています。

## 環境

AWS Lambda(python3.11)

## 導入方法

<br>
1. LINE Developers の公式サイトにアクセスし、LINE のシークレットキー、LINE のトークン ID を取得します。
https://developers.line.biz/ja/

<br>
2. AWSのlambdaに新規関数作成
<br>
lambdaに関数を作成するとコードにlamda_function.pyが自動生成されます。
このコードに本ファイル「lambda_function.py」の内容をコピーして貼り付けてください。
<br>
<br>
3. 3で作成した関数にトリガー（API Gateway）を追加。<br>
　　このGatewayに割り当たっているロールに対し権限をあたえる。<br>
   →「AmazonRekognitionFullAccess」を追加する事。
   　<br>今回Rekognitionを使用するため。
<br>
作成した際にできたAPI endpointはLINEのWebhook URLにコピーする。
<br>
<br>
4. レイヤーを追加
<br>
