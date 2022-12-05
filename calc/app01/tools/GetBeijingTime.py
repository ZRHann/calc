# 获取网络时间

import time
import requests
import json
from datetime import datetime


def getBeijingTime():
    # HTTP客户端运行的浏览器类型的详细信息。通过该头部信息，web服务器可以判断到当前HTTP请求的客户端浏览器类别。
    hea = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'} #站点服务器认为自己（浏览器）兼容Moailla的一些标准
    # 设置访问地址，我们分析到的；
    url = r'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
    # 用requests get这个地址，带头信息的；
    r = requests.get(url=url, headers=hea)
    # 检查返回的通讯代码，200是正确返回；
    if r.status_code == 200:
        data = r.text
        timeStamp = int(json.loads(data)['data']['t']) // 1000
        styleTime = datetime.fromtimestamp(timeStamp)
        return styleTime
    else:
        return "Time Request Error"

