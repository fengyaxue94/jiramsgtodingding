import time
import requests
import json
import base64
import hashlib
import hmac
import time
import urllib
import sys
# 机器人设置中webhook后的access_token
TOKEN = "e7f4961810af7e5e293ef9aac0f3cf81549925d8b76b4363654ba1b9e88c6db2"
# 安全设置中的秘钥
SECRET = "SECd21b3ec435f9ebbb2c50da01dbf3bfbaa77a6fabebb3eb48e854cbe1f71a564e"
headers = {'Content-Type': 'application/json;charset=utf-8'}

def get_url():
    # 钉钉官方要求，请求的url中必须携带三个参数，access_token， timestamp，sign(签名是由secret加密而来)
    timestamp = str(round(time.time() * 1000))
    #secret = 'this is secret'
    secret_enc = SECRET.encode('utf-8')
    string_to_sign ='{}\n{}'.format(timestamp, SECRET)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # 完整的url
    api_url = "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(TOKEN, timestamp, sign)
    return api_url

if __name__ == "__main__":
    # 发送的消息类型可查看文档，此处只做测试
    dingurls = get_url()
    print(dingurls)
    msgs = {
        "msgtype": "text",
        "text": {
            "content": "闲聊，一条消息5毛钱，概不赊账@18221010405"

        },
        "at": {
            "atMobiles": [
                "13120095528",
                "18221010405"
            ]
        }
    }
    res = requests.post(dingurls, headers=headers, json=msgs)
    print(res)