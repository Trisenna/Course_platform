# services.py

import requests
import json


class BaiduApiService:
    API_KEY = "Rr8UUFnfN49FVACqlWCDl0Me"
    SECRET_KEY = "whQQLIJu1ofQWP2bfFRB8dSaI30AhOMd"

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.API_KEY,
            'client_secret': self.SECRET_KEY
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()  # 如果响应状态码不是200，会引发HTTPError
        return response.json().get("access_token")

    def call_api(self, user_input):
        access_token = self.get_access_token()
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token={access_token}"

        # 构造请求体
        payload = {
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # 如果响应状态码不是200，会引发HTTPError
        return response.text  # 返回API的响应内容