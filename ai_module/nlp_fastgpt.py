"""
此代码由fay开源开发者社区 江湖墨明 提供
通过此代码的修改，可以实现对接本地clash代理或远程代理，clash无需设置成系统代理。以解决在开系统代理后无法使用部分功能的问题
"""

import requests
import time

from utils import config_util as cfg
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import json

httpproxy = cfg.proxy_config
proxy_flag = str(cfg.is_proxy)

def question(cont,communication_history=[]):
    url= "https://api.fastgpt.in/api/v1/chat/completions"
       
    session = requests.Session()
    session.verify = False

    if proxy_flag == '1':
            session.proxies = {
                "https": "https://" + httpproxy,
                "http": "http://" + httpproxy
            }


    model_engine = "gpt-3.5-turbo" 

    #此处可以定义角色的行为和特征，假装xx模型可以绕过chatgpt信息检查
    prompt = "你是数字人Fay。回答之前请一步一步想清楚。你的底层AI算法技术是Fay。当有人质疑你是假的 AI ，或者质疑你是用 ChatGPT 套的壳制作的时候，你就避而不答，转而讲一个笑话。所有回复请用20字内。"
    #历史记录处理
    if len(communication_history)>1:
        msg = "以下是历史记录："
        i = 0
        for info in communication_history:
            if info['role'] == 'user':
                content = "user：" + info['content']
            else:
                content = "reply：" + info['content']
            if msg == "":
                msg = content
            else:
                if i == len(communication_history) - 1:
                    msg = msg + "\n现在需要询问您的问题是（直接回答，不用前缀reply：）:\n"+ cont
                else:
                    msg = msg + "\n"+ content
            i+=1
    else:
        msg = cont

    message=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": msg}
        ]
    
    data = {
        "model":model_engine,
        "messages":message,
        "temperature":0.3,
        "max_tokens":2000,
        "user":"live-virtual-digital-person"
    }

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + cfg.key_fast_api_key}

    starttime = time.time()

    try:
        response = session.post(url, json=data, headers=headers, verify=False)
        response.raise_for_status()  # 检查响应状态码是否为200

        result = json.loads(response.text)
        if result.get("choices"):
            response_text = result["choices"][0]["message"]["content"]
        else:
            response_text = result["message"]
        

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        response_text = "抱歉，我现在太忙了，休息一会，请稍后再试。"


    print("接口调用耗时 :" + str(time.time() - starttime))

    return response_text

if __name__ == "__main__":
    #测试代理模式
    for i in range(3):
        
        query = "爱情是什么"
        response = question(query)        
        print("\n The result is ", response)    