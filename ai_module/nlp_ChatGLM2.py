import json
import requests
def question(cont,communication_history):
    content = {
        "prompt":"请简单回复我。" +  cont,
        "history":communication_history}
    url = "http://127.0.0.1:8000"
    req = json.dumps(content)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, headers=headers, data=req)
    res = json.loads(r.text).get('response')
    return res

