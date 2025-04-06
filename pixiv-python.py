from flask import Flask, redirect, make_response
from bs4 import BeautifulSoup
import requests
import json

headers = {
    "cookie": "",    #若要抓取R-18和R-18G，需在此处填写cookie
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net/"
}

app = Flask(__name__)

@app.route('/<path:path>', methods=['GET', 'POST'])
def image(path):
    #解析请求
    if '-' in path and '.' in path:
        pid = path.split('-')[0]
        pNum = str(int(path.split('-')[1].split('.')[0]) - 1)
        fileEx = path.split('-')[1].split('.')[1]
    elif '-' in path:
        pid = path.split('-')[0]
        pNum = str(int(path.split('-')[1]) - 1)
    elif '.' in path:
        pid = path.split('.')[0]
        fileEx = path.split('.')[1]
    else:
        pid = path

    #忽略https证书错误，因为反代后非原证书
    requests.packages.urllib3.disable_warnings()
    #请求id对应的ajax api
    response = requests.get(f"https://www.pixiv.net/ajax/illust/{pid}/pages?lang=zh", headers=headers, verify=False)
    if not response.ok:
        #若失败则返回对应状态码
        return make_response('', response.status_code)
    else:
        #若成功则分析api中的原图网址并重定向为反代网址
        html = response.content
        content = json.loads(html)
        url = content['body'][0]['urls']['original'].replace("i.pximg.net", "localhost:8080")

        if 'pNum' in locals().keys() and 'fileEx' in locals().keys():
            url = url.replace('_p0.', f'_p{pNum}.')
            url = url.replace('_ugoira0.', f'_ugoira{pNum}.')
            url = url.rsplit('.', 1)[0] + f'.{fileEx}'
        elif 'pNum' in locals().keys():
            url = url.replace('_p0.', f'_p{pNum}.')
            url = url.replace('_ugoira0.', f'_ugoira{pNum}.')
        elif 'fileEx' in locals().keys():
            url = url.rsplit('.', 1)[0] + f'.{fileEx}'

        return redirect(f'{url}')

if __name__ == '__main__':
    app.run(port=8088)
