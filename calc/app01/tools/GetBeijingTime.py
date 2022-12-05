# 获取网络时间

import time
import requests
import json
from datetime import datetime


def getBeijingTime():
    from datetime import datetime
    from datetime import timedelta
    from datetime import timezone

    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )

    # # 协调世界时
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    # print("UTC:")
    # print(utc_now, utc_now.time())
    # print(utc_now.date(), utc_now.tzname())

    # 北京时间
    beijing_now = utc_now.astimezone(SHA_TZ)
    # print("Beijing:")
    # print(beijing_now)
    # print(beijing_now.time())
    # print(beijing_now.date())
    # print(beijing_now.tzname())

    # # 系统默认时区
    # local_now = utc_now.astimezone()
    # print("Default:")
    # print(local_now, local_now.time())
    return beijing_now.strftime('%Y-%m-%d %H:%M:%S')



