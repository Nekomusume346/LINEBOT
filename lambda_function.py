"""
rekognitionを用いたLine Bot感情分析
"""

import os
import glob

from linebot.lambda_function import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,VideoMessage
)

import boto3

client = boto3.client('rekognition')

LINE_CHANNEL_SECRET = 'ここにLINEのシークレットキー'
LINE_CHANNEL_ACCESS_TOKEN = 'ここにLINEのトークンID'

handler = WebhookHandler(LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


def lambda_handler(event, context):
    headers = event["headers"]
    body = event["body"]

    # get X-Line-Signature header value
    signature = headers['x-line-signature']

    # handle webhook body
    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}

#レスポンス結果からどのくらいの笑顔なのか判定してメッセージを返す
def happy(result):
    strmessage = ""
    cont = 0
    if len(result["FaceDetails"]) == 0:
        strmessage = "顔が検出できないわ。"
    else:
        for detail in result["FaceDetails"]:
            if len(detail["AgeRange"]) > 0:
                cont = cont + 1
                
            if most_confident_emotion(detail["Emotions"]) == "HAPPY":
                strmessage = "最高の笑顔ね。その調子よ。"
            elif most_confident_emotion(detail["Emotions"]) == "CALM":
                strmessage =  "ちょっと笑顔が足りないわね。"
            elif most_confident_emotion(detail["Emotions"]) == "SAD":
                strmessage =  "悲しい顔しているようね。笑顔が大事よ。もっと笑って。"
            elif most_confident_emotion(detail["Emotions"]) == "ANGRY":
                strmessage =  "怒っているなんてもったいないわね。"
            elif most_confident_emotion(detail["Emotions"]) == "SURPRISED":
                strmessage =  "あら？何に驚いているの？"
            elif most_confident_emotion(detail["Emotions"]) == "DISGUSTED":
                strmessage =  "うんざりしているように見えるわ。"
            elif most_confident_emotion(detail["Emotions"]) == "FEAR":
                strmessage =  "何を怖がっているの？"
            else:
                strmessage = "うーん、この写真よくわからないわね。"
        
        if cont > 1:
            strmessage = "ごめんなさい。一人しか分析できないのよ。"
            
    return strmessage
    

#"Emotions"に入っている感情のうち最もConfidencs（確信）が高いものを返す
def most_confident_emotion(emotions):
    max_conf = 0
    result = ""
    for e in emotions:
        if max_conf < e["Confidence"]:
            max_conf = e["Confidence"]
            result = e["Type"]
    return result

#メッセージがテキストだった時の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """ TextMessage handler """
    #下記を有効にするとオウム返しになる。
    #input_text = event.message.text
    input_text = "メッセージは処理できないのよ。画像を送ってくれるかしら。一人で写っている写真を送ってちょうだい。"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=input_text))

#メッセージが画像だったときの処理
@handler.add(MessageEvent, message=ImageMessage)
def handle_Image_message(event):
    #ユーザーから送られてきた画像を保存　lambdaではtmpの下でないと書き込みできないので注意する
    massage_content = line_bot_api.get_message_content(event.message.id)
    file_path = "/tmp/sent-image.jpg"
    with open(file_path, 'wb') as fd:
        for chnk in massage_content.iter_content():
            fd.write(chnk)


    #バイナリーファイルで開く rb
    with open(file_path, 'rb') as fd:
        sent_image_binary = fd.read()
        #Rekognitionで感情分析（detect_faces関数を使用）
        #第一引数はBytesかS3どちらか指定。AttributesをALLにすると詳細な分析を受け取れる。
        response = client.detect_faces(Image = {"Bytes": sent_image_binary}, Attributes = ["ALL"] )
    
    #print(response)

    message = happy(response)

    #ユーザーに送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(message)))


    #画像が不要になったので削除
    #os.remove(file_path)
    
    #tmpファイルを全削除
    cleartmp()

#メッセージが動画だった時の処理
@handler.add(MessageEvent, message=VideoMessage)
def handle_Video_message(event):
    cleartmp()
    input_text = "ごめんなさい。動画は処理できないのよ。画像を送ってくれるかしら。一人で写っている写真をお願いね。"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=input_text))


#tmpファイルを全削除
def cleartmp():
    for p in glob.glob('/tmp/' + '*'):
       if os.path.isfile(p):
           os.remove(p)