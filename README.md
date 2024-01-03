# 笑顔判定ボット

## このアプリの目的

LINE から人物が写った画像を送ることにより、その表情から感情分析した結果を BOT として返します。<br>
AWS Rekognition を使った画像処理を体験する事ができます。<br>
体験することが目的のため仕様は簡単にしています。<br>
メッセージに対しては対応していません。<br>

## 環境

AWS Lambda(python3.11), Amazon Rekognition,
LINE Developers

## 導入方法

### STEP1

#### LINE Developers の公式サイトにアクセスし、LINE のシークレットキー、LINE のトークン ID を取得します。

### STEP2

#### AWS の lambda に新規関数作成

lambda に関数を作成するとコードに lamda_function.py が自動生成されます。
このコードに本ファイル「lambda_function.py」の内容をコピーして貼り付けてください。

### STEP3

#### 2 で作成した関数にトリガー（API Gateway）を追加

この Gateway に割り当たっているロールに対し権限をあたえる。<br>
→「AmazonRekognitionFullAccess」を追加する事。
<br>
作成した際にできた API endpoint は LINE の Webhook URL にコピーする。

### STEP4

#### レイヤーを追加
