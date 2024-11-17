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
ORCHESTRATE_API_KEY = 'eyJraWQiOiJHQmhKTU83NFRRM2dOeXBHUWhEN2txMTVfcE14dGZ3ZFIya2dYN1QyczZ3IiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL3NpdXNlcm1ndG1zLW1zcC11c2VyLW1hbmFnZXIuYXBwcy5hcC1kcC0wMDEua29oMy5wMS5vcGVuc2hpZnRhcHBzLmNvbS9zaXVzZXJtZ3IvYXBpLzEuMCIsImF1ZCI6ImNybjp2MTphd3M6cHVibGljOnd4bzp1cy1lYXN0LTE6c3ViLzIwMjQwNTE0LTA2NDAtMTUzOC0zMDBjLWFhM2M1NGU4Y2MxYzoyMDI0MDUxNC0xMzM1LTIxODItOTAzZi02MjRhZjY5YzdiZGE6OiIsImV4cCI6MTczMTg2NTA1NywianRpIjoiRUJ3QktrYWhEeEh6M2Q3RHVmSFlMdyIsImlhdCI6MTczMTg1Nzg1NywibmJmIjoxNzMxODU3ODI3LCJ0ZW5hbnRJZCI6IjIwMjQwNTE0LTEzMzUtMjE4Mi05MDNmLTYyNGFmNjljN2JkYSIsInN1YnNjcmlwdGlvbklkIjoiMjAyNDA1MTQtMDY0MC0xNTM4LTMwMGMtYWEzYzU0ZThjYzFjIiwic3ViIjoiZTMyYTk3NTItYzc2Ny0zMzU4LTgxZTktYjA5Y2MwOTA3ZjNiIiwiZW50aXR5VHlwZSI6IlVTRVIiLCJlbWFpbCI6ImF1c3Rpbi5odWFuZ0BpYm0uY29tIiwibmFtZSI6ImF1c3Rpbi5odWFuZ0BpYm0uY29tIiwiZGlzcGxheW5hbWUiOiJhdXN0aW4uaHVhbmdAaWJtLmNvbSIsImlkcCI6eyJyZWFsbU5hbWUiOiJjbG91ZElkZW50aXR5UmVhbG0iLCJpc3MiOiJodHRwczovL3dvLWlibS1wcm9kLnZlcmlmeS5pYm0uY29tL29pZGMvZW5kcG9pbnQvZGVmYXVsdCJ9LCJncm91cHMiOltdLCJyb2xlcyI6WyJCdWlsZGVyIl0sImlkcFVuaXF1ZUlkIjoiNjQ2MDAwNjZVVSJ9.cV9FyUxqUVow35HeXJLn4ImtpXKpskNhccOX8JRAlwPAZxGq-65kNYDsvQiLYbpl0LMi4utfdBbLm57sjMXQ4WWTbMmkE6zhoPBYo3oACNJoU8XWBguP2NCkTktWpp8o2jlTGC-LvxdUBzgjLEewr6_S1R6LeWaxiIyUCXuLhPDNZz1SvHplI2J2t9I5wXRBd1pSXDNdF4s-ffg0V6_u-ny53WiWlOS1-x7Qz84l0OTfJbgCJln1pVu69lJVIgoh4_A6vj78KeSOb6mKryXqONPrPVZLMJjqgDmLjotp-eZ4qFIlCDiNCTgzIH_mazrzi4Om6j2XYjcC0CYYiVQ0hg'  # 將此處替換為你在 Watson Orchestrate 中找到的 API Key
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




