import json

import requests
from flask import Flask, request, jsonify, render_template, current_app

app = Flask(__name__)

h = """
Host: www.tantanjiujiu.com
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://www.tantanjiujiu.com/tantanjiujiu/bookinfo/jckj
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: advanced-frontend=hfojufhdt5domgj558h9jmaopv; _identity-frontend=d0eb15a18351cdafb8a30019b27b8df7aec17167abaf4e6d230bf10726c56d79a%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A48%3A%22%5B13377%2C%22MXyXpaOGONSHSIlQ_VfhMSKH7RkYrCsK%22%2C86400%5D%22%3B%7D; _csrf-frontend=672ade7f688c4284edb2016ecd16c93cae5ca2ec2273a26a5eb71cc3ff838830a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22jSYha1kEaW8qw4GhY3j6WAlwt-UoDn-E%22%3B%7D
"""
h = dict(line.split(': ') for line in h.strip().split('\n'))



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
        headers=h,
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
