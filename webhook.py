#!/usr/bin/env python
# coding: utf-8

# In[1]:

from flask import Flask, request, abort
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

LINE_CHANNEL_SECRET = 'a2d2ca9655fcb15f5fd44cc3d22e8abe'
LINE_CHANNEL_ACCESS_TOKEN = 'VGo0+6xogtABPzeMFePwunhUoZx5zC5hOmaK+J7+KIDLDohDL14aKGm7yCFKFVJ7Bz70+rGWLrOvgAY3CmDqdnXUQpzLJaoWm9Gb205IYPTiZVytMLv74xAJlo02IFzFx2xQWUH/mhN+U7CDwddpQgdB04t89/1O/w1cDnyilFU='
ORCHESTRATE_API_KEY = 'azE6dXNyX2UzMmE5NzUyLWM3NjctMzM1OC04MWU5LWIwOWNjMDkwN2YzYjpXbUdoY1pWWUQ5MzUvVDZIOTJwbW53bVA1QzBkTU9yb0VROHBmN3BnRndJPTo4WVhh'  # 將此處替換為你在 Watson Orchestrate 中找到的 API Key
ORCHESTRATE_API_URL = 'https://api.us-east-1.aws.watsonassistant.ibm.com/instances/20240514-1335-2182-903f-624af69c7bda'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text

    # 呼叫 Watson Orchestrate AI Assistant API
    response = requests.post(
        f'{ORCHESTRATE_API_URL}/message',
        json={
            'input': {
                'text': message
            }
        },
        headers={
            'Authorization': f'Bearer {ORCHESTRATE_API_KEY}',  # 將 API Key 添加到 headers 中
            'Content-Type': 'application/json'
        }
    )

    # 取得 AI Assistant 的回應
    result = response.json()['output']['generic'][0]['text']

    # 透過 LINE 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result)
    )

if __name__ == '__main__':
    app.run()
    



# In[ ]:




