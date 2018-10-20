# 文件timerStartDaily.py

import os
import time
import datetime
import shutil
from scrapy import cmdline


recoderDir = r"job_info"            # 这是为了爬虫能够续爬而创建的目录，存储续爬需要的数据
checkFile = "isRunning.txt"         # 爬虫是否在运行的标志

startTime = datetime.datetime.now()
print(f"startTime = {startTime}")

i = 0
hours = 0
while True:
    isRunning = os.path.isfile(checkFile)
    if not isRunning:
        """
        爬虫不在执行，开始启动爬虫
        在爬虫启动之前处理一些事情，清掉JOBDIR = job_info
        """
        isExsit = os.path.isdir(recoderDir)  # 检查JOBDIR目录job_info是否存在
        print(f"Weibo_Spider is  not running, ready to start. isExsit:{isExsit}")
        if isExsit:
            removeRes = shutil.rmtree(recoderDir)  # 删除续爬目录job_info及目录下所有文件
            print(f"At time:{datetime.datetime.now()}, delete res:{removeRes}")
        else:
            print(f"At time:{datetime.datetime.now()}, Dir:{recoderDir} is not exsit.")
        time.sleep(20)
        crawlerTime = datetime.datetime.now()
        waitTime = crawlerTime - startTime
        print(f"At time:{crawlerTime}, start crawler: Weibo_Spider !!!, waitTime:{waitTime}")
        cmdline.execute('scrapy crawl weibo -s JOBDIR=job_info/weibo'.split())
        break
    else:
        """
        爬虫在执行
        """
        print(f"At time:{datetime.datetime.now()}, Weibo_Spider is running, sleep to wait.")
    i += 1
    time.sleep(600)       # 每隔10分钟，检查一下爬虫的运行状态
    hours += 10
    if hours >= 1440:     # 等待满24小时，自动退出监控脚本
        break
