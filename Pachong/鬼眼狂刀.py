import multiprocessing
import os
import re
from os import path

import requests
from bs4 import BeautifulSoup


def gethtml(ary):

    for  ele in ary:

        cannext = True
        index = 0

        while cannext == True:

            suburl = url + ele.a.get('href') + 'index_' + str(index) + '.html'
            urlresponse = requests.get(suburl)
            index += 1

            # 中断
            if urlresponse.status_code != 200:
                cannext = False

            htmlStr = urlresponse.text
            reg = r'(?<=var mhurl1="13/' + ele.a.get('href') + ').*\.jpg'
            imgindex = re.findall(reg, htmlStr)

            dirpath = path.dirname(__file__) + '/鬼眼狂刀' + '/' + ele.a.get('title')
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)

            if len(imgindex) > 0:
                imgurl = "http://p0.manhuapan.com/13/" + ele.a.get('href') + imgindex[0]
                img = requests.get(imgurl).content

                # print(imgurl)

                with open(dirpath + '/' + str(index) + '.jpg', 'wb') as f:
                    f.write(img)
                    f.close()
                    print(ele.a.get('title') + '  第' + str(index) + '保存成功  ' + 'url= ' + imgurl)


if __name__ == '__main__':

    url = "https://manhua.fzdm.com/13/"

    response = requests.get(url).text

    soup = BeautifulSoup(response, 'lxml')

    ary = soup.findAll('li', class_='pure-u-1-2 pure-u-lg-1-4')
    # 逆序
    ary.reverse()

    #其它的都下完了
    # ary = ary[20:30]

    processNum = 5
    aryLenth = int(len(ary) / processNum)

    for i in range(processNum):
        # 分割成n个数组
        subary = []
        if i == processNum - 1:
            subary = ary[i * aryLenth:]
        else:
            subary = ary[i * aryLenth:(i + 1) * aryLenth]

        # 开始每个小任务
        p = multiprocessing.Process(target=gethtml, args=(subary,))
        p.start()
