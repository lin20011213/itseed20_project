from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import keep_alive

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('YF3wXGsqCUQ8wdWvkcnof7YwTHViKj+rMyeDFCGLNdKf4Ykx5RW6l5SaWcXe8+6mwcGZ6TiVoNmobKfgiTF9dqkf2ruUh1OjluMttZ8cBi2/C268kA3jEHEp/+IJluzkVp92gfdkkqgPK0/z7PEw+FI9PbdgDzCFqoOLOYbqAITQ=')
# Channel Secret
handler = WebhookHandler('47d1b94f35974d2583e5b109c097e665')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    keep_alive.keep_alive()
    app.run(host='0.0.0.0', port=port)
