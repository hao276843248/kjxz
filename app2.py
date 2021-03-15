import json

import requests
from flask import Flask, request, jsonify, render_template, current_app

app = Flask(__name__)


@app.route('/')
def index():
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
    # http://www.tantanjiujiu.com/tantanjiujiu/bookinfo/showkejian?type=LXYYZW&nianji=3X&danyuan=2&kewenxuhao=1&id=4670
    url = url.split("?")[1]
    urls = url.split("&")
    urls = list(filter(lambda i: "id" in i, urls))[0]
    ids = urls.split("=")[1]
    rets = []
    r2 = requests.post(
        f"http://www.tantanjiujiu.com/tantanjiujiu/bookinfo/jiancha",
        data={"kejianurl": ids}
    )
    allData = json.loads(r2.text)
    url = "http://www.tantanjiujiu.com"
    if allData["kejianurl"]:
        rets.append({"name": "课件", "url": url + allData["kejianurl"]})
    if allData["jiaoxuesheji"]:
        rets.append({"name": "教学设计", "url": url + allData["jiaoxuesheji"]})
    if allData["xbpaper"]:
        rets.append({"name": "学霸小测", "url": allData["xbpaper"]})
    if not rets:
        rets.append({"name": "解析错误", "url": ""})
    print(rets)
    return jsonify(rets)


if __name__ == '__main__':
    app.run()
