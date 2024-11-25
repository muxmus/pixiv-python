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

    requests.packages.urllib3.disable_warnings()
    response = requests.get(f"https://www.pixiv.net/artworks/{pid}", headers=headers, verify=False)
    if response.status_code != 200:
        return make_response('', response.status_code)
    else:
        html = response.content

        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find('meta', id='meta-preload-data')

        jsonData = links.get('content')
        content = json.loads(jsonData)
        url = content['illust'][f'{pid}']['urls']['original'].replace("i.pximg.net", "i.muxmus.com:5000")

        if 'pNum' in locals().keys() and 'fileEx' in locals().keys():
            url = url.replace('_p0.', f'_p{pNum}.')
            url = url.rsplit('.', 1)[0] + f'.{fileEx}'
        elif 'pNum' in locals().keys():
            url = url.replace('_p0.', f'_p{pNum}.')
        elif 'fileEx' in locals().keys():
            url = url.rsplit('.', 1)[0] + f'.{fileEx}'

        return redirect(f'{url}')

if __name__ == '__main__':
    app.run(port=7000)
