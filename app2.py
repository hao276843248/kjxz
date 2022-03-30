import json
import logging
import re

import requests
from flask import Flask, request, jsonify, render_template, current_app, g

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
url = "http://www.tantanjiujiu.com/tantanjiujiu/site/login"
loginsendmsg = "http://www.tantanjiujiu.com/tantanjiujiu/site/loginsendmsg"
r_session=None

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://www.tantanjiujiu.com',
    'Referer': 'http://www.tantanjiujiu.com/tantanjiujiu/bookinfo/showkejian?type=ZTYD&nianji=4X&danyuan=5&kewenxuhao=17&id=1491',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


@app.route('/')
def index():
    global r_session
    r_session = login_sign()
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    # 静态路径访问的模拟默认实现，send_static_file
    return current_app.send_static_file('news/tan.ico')


@app.route('/passHtml', methods=["POST"])
def passHtml():
    url = request.json.get("url")
    if not url:
        return jsonify([])
    rets = []
    try:
        # http://www.tantanjiujiu.com/tantanjiujiu/bookinfo/showkejian?type=LXYYZW&nianji=3X&danyuan=2&kewenxuhao=1&id=4670
        url = url.split("?")[1]
        urls = url.split("&")
        urls = list(filter(lambda i: "id" in i, urls))[0]
        ids = urls.split("=")[1]

        data = {
            'kejianurl': ids,
        }
        session = r_session
        r2 = session.post('http://www.tantanjiujiu.com/tantanjiujiu/bookinfo/jiancha', headers=headers,
                           data=data, verify=False)
        allData = json.loads(r2.text)
        url = "http://www.tantanjiujiu.com"
        log.info(allData)
        if allData["kejianurl"]:
            urls = allData["kejianurl"]
            if ("tantanjiujiu.com" not in allData["kejianurl"]):
                urls = url + allData["kejianurl"]
            rets.append({"name": "课件", "url": urls, "username": allData["username"]})
        if allData["jiaoxuesheji"]:
            urls = allData["jiaoxuesheji"]
            if ("tantanjiujiu.com" not in allData["jiaoxuesheji"]):
                urls = url + allData["jiaoxuesheji"]
            rets.append({"name": "教学设计", "url": urls, "username": allData["username"]})
        if allData["xbpaper"]:
            urls = allData["xbpaper"]
            if ("tantanjiujiu.com" not in allData["xbpaper"]):
                urls = url + allData["xbpaper"]
            rets.append({"name": "学霸小测", "url": urls, "username": allData["username"]})
        if not rets:
            rets.append({"name": "解析错误", "url": ""})
        log.info(rets)
    except Exception as e:
        log.error(e)
    return jsonify(rets)

import random

def raddomPhone():
    headList = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
               "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
               "186", "187", "188", "189"]
    return (random.choice(headList) + "".join(random.choice("0123456789") for i in range(8)))


def login_sign():
    r_session = requests.session()
    page = r_session.get(url)
    reg = r'<input type="hidden" name="_csrf-frontend" value="(.+)">      <div class="form-group field-loginform-username required">'
    csrf = re.findall(reg, page.text)[0]
    phone = raddomPhone()
    post = r_session.post(loginsendmsg, data={"bianhao": phone})
    data = {
        "_csrf-frontend": csrf,
        "LoginForm[username]": phone,
        "pnum": post.text,
        "LoginForm[rememberMe]": "0",
        "login-button": ""
    }
    # 完成用户登录
    response1 = r_session.post(url, data=data, headers=headers)
    print(response1.content)  # 这里可以看到是否模拟登陆成功
    return r_session



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4900)
