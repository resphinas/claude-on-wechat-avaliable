import requests

import requests


def get_response(prompt):
    try:
        url = "http://sdly.blockelite.cn:17351"  # 替换为实际的URL
        headers = {'Content-Type': 'application/json'}
        payload = {'prompt': prompt, 'history': []}

        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            return response_data['response']
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

prompt = "你好"
response = get_response(prompt)
print(response)