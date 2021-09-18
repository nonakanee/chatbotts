'''
# file location /home/saitarn15d/project1/project1.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello, Flask application.</h1>"

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)

    app.run(host='127.0.0.1',port=5000,debug=False,ssl_context='adhoc')

    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(host='127.0.0.0',port=port,debug=False,threaded=True)

    app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)

import ssl
context = ssl.SSLContext()
context.load_cert_chain('ssl/server.crt', 'ssl/server.key')
'''

from flask import Flask
from flask import request
from flask import abort
import requests
import json

app = Flask(__name__)
@app.route('/', methods=['POST','GET'])

def webhook():
    if request.method == 'POST':
        payload = request.json
        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)

        if 'good' in message :
            Reply_messasge = 'very good'
            ReplyMessage(Reply_token,Reply_messasge,'eE6RC+Z8qA1L/xAt+eK80C3sovJbD2sy4cv7A9oFrRWGUm5zjXkGQHrghIkmZdTfrS1TTBeBN/OLu/qHTEWImDuQ4Rcjcd5lM/B/UYci3oThRE4n1IKKdZUTPXtmLKj8b2rRqbdAd7T7SJ7FCn/M4AdB04t89/1O/w1cDnyilFU=') #Channel access token

        return request.json, 200
    else:
        abort(400)

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }
    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200

if __name__ == '__main__':
    app.run(debug=False)
    '''app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)'''