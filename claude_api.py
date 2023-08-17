from config import conf, load_config
import requests
import json
import re
import time
import execjs

class Claude:
    def __init__(self,org_uuid,con_uuid,cookie):
        self.org_uuid = org_uuid
        self.con_uuid = con_uuid
        self.cookie = cookie
        self.ctx = execjs.compile(open('decode.js',encoding='utf-8').read())

    def send_message(self, query):
        sentry_trace = self.ctx.call('Sentry_Trace')
        traceid = sentry_trace.split("-")[0]
        url = "https://claude.ai/api/append_message"
        payload = json.dumps({
            "completion": {
                "prompt": query,
                "timezone": "Asia/Singapore",
                "model": "claude-2",
            },
            "organization_uuid": self.org_uuid,
            "conversation_uuid": self.con_uuid,
            "text": query,
            "attachments": []
        })

       
        headers = {
            'Accept': 'text/event-stream, text/event-stream',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': self.cookie,
            'Origin': 'https://claude.ai',
            'Pragma': 'no-cache',
            'Referer': 'https://claude.ai/chat/c462f2ba-e0c6-4344-b790-649d837908b1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
            'baggage': f'sentry-environment=production,sentry-release=86abdb3b7746a7db1186e7f95122841d382471e3,sentry-public_key=58e9b9d0fc244061a1b54fe288b0e483,sentry-trace_id={traceid}',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sentry-trace': sentry_trace
        }
        print(headers)
        print("here")
        try:
            s = requests.session()
            response = s.post(url, headers=headers, data=payload,stream = True)
            # response = requests.request("POST", url, headers=headers, data=payload,stream = True)
            # print(response.headers,"\n",response.cookies,"\n",response.text)
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

        response = requests.request("GET", url, headers=headers)
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
            # print(history)
            # print(history)

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
    org_uuid= ###
    con_uuid= ###
    cookie = ###
    # claude = Claude(org_uuid, con_uuid,cookie)
    # history = claude.chat_conversation_history()
    # print(history)
    main(org_uuid,con_uuid,cookie)
