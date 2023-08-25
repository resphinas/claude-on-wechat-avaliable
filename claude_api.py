import json
import time
from curl_cffi import requests

# 定义代理服务器的地址
proxy_url = "http://127.0.0.1:33210"

# 构建代理字典，键是协议（http、https等），值是代理服务器地址
proxies = {
    "http": proxy_url,
    "https": proxy_url
}
class Claude:
    def __init__(self,org_uuid,con_uuid,cookie):
        self.org_uuid = org_uuid
        self.con_uuid = con_uuid
        self.cookie = cookie

    def send_message(self, query):
        # sentry_trace = self.ctx.call('Sentry_Trace')
        # traceid = sentry_trace.split("-")[0]
        url = "https://claude.ai/api/append_message"
        payload = json.dumps({
            "completion": {
                "prompt": f"{query}",
                "timezone": "Asia/Kolkata",
                "model": "claude-2"
            },
            "organization_uuid": f"{self.org_uuid}",
            "conversation_uuid": f"{self.con_uuid}",
            "text": f"{query}",
            "attachments": []
        })
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/event-stream, text/event-stream',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Origin': 'https://claude.ai',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

        try:
            response = requests.post(url, headers=headers, data=payload,impersonate="chrome110",proxies=proxies,timeout=400)
            print(response.text)
        except Exception as error:
            print(error)
            return False

        if len(response.text) >=60:
            return True
        return False

    def chat_conversation_history(self):
        url = f"https://claude.ai/api/organizations/{self.org_uuid}/chat_conversations/{self.con_uuid}"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}'
        }

        response = requests.get( url, headers=headers, proxies =proxies,impersonate="chrome110")
        response.encoding = 'utf-8'
        return response.json()

def get_last_answer(history,cache):

    max_index = 0
    for i in history["chat_messages"]:
        if i["index"] > max_index:
            max_index = i["index"]
            body = i
    if max_index not in cache:
        cache.append(max_index)
        answer = body["text"]
        return answer,cache
    return None,cache

def main(org_uuid,con_uuid,cookie):

    claude = Claude(org_uuid, con_uuid,cookie)
    cache = []
    while True:
        query = input("human:")

        result = claude.send_message(query)
        if result:
            print("send success")
        else:
            continue

        try_time_current = 0

        #最大重试次数
        try_time_max = 5

        while True:

            history = claude.chat_conversation_history()
            answer,cache = get_last_answer(history, cache)
            print("cache :" ,cache)
            if answer == None or answer == query:
                time.sleep(1)
                try_time_current += 1
                if try_time_current > try_time_max:
                    answer = "消息获取失败"
                    break
                continue

            else:
                break

        print("robot: ", answer)



if __name__ == '__main__':
    pass
    # org_uuid= ###测试时取消注释
    # con_uuid= ###
    # cookie = ###
    # claude = Claude(org_uuid, con_uuid,cookie)
