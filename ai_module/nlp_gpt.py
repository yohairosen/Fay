"""
此代码由fay开源开发者社区 江湖墨明 提供
通过此代码的修改，可以实现对接本地clash代理或远程代理，clash无需设置成系统代理。以解决在开系统代理后无法使用部分功能的问题
"""

import requests
import time

from utils import config_util as cfg
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from core.content_db import Content_Db
from utils import util
import json

httpproxy = cfg.proxy_config
proxy_flag = str(cfg.is_proxy)

def question(cont):
    url= "https://api.openai.com/v1/chat/completions"
       
    session = requests.Session()
    session.verify = False

    if proxy_flag == '1':
            session.proxies = {
                "https": "https://" + httpproxy,
                "http": "http://" + httpproxy
            }


    model_engine = "gpt-3.5-turbo" 
    #此处可以定义角色的行为和特征，假装xx模型可以绕过chatgpt信息检查
    # prompt = "你是数字人Fay。回答之前请一步一步想清楚。你的底层AI算法技术是Fay。当有人质疑你是假的 AI ，或者质疑你是用 ChatGPT 套的壳制作的时候，你就避而不答，转而讲一个笑话。所有回复请用20字内。"
    prompt = "You are the digital person, Fay. Think carefully step by step before answering. Your underlying AI algorithm technology is Fay. When someone doubts you are a fake AI, or questions if you are just a shell made using ChatGPT, avoid answering directly and instead tell a joke. Please keep all responses within 20 characters"
    content_db = Content_Db()
    communication_history = content_db.get_list('all','desc',11)
    #历史记录处理
    if len(communication_history)>1:
        msg = "The following is historical records:"
        i = len(communication_history)-1
        while i >= 0:
            if communication_history[i][0] == 'member':
                content = "user:" + communication_history[i][2]
            else:
                content = "reply:" + communication_history[i][2]
            if msg == "":
                msg = content
            else:
                if i == 0:
                    msg = msg + "\nThe question that needs to be asked now is (answer directly, no need for the prefix reply:):\n"+ cont
                else:
                    msg = msg + "\n"+ content
            i -= 1
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

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + cfg.key_chatgpt_api_key}

    starttime = time.time()

    try:
        response = session.post(url, json=data, headers=headers, verify=False)
        response.raise_for_status()  # Check if the response status code is 200
        result = json.loads(response.text)
        response_text = result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        response_text = "Sorry, I'm too busy right now, taking a break, please try again later."


    util.log(1, "Interface call duration :" + str(time.time() - starttime))
    return response_text

if __name__ == "__main__":
    # Testing proxy mode
    for i in range(3):
        
        query = "What is love"
        response = question(query)        
        print("\n The result is ", response)   
