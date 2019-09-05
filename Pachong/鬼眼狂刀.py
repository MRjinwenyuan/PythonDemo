import os
import re
from os import path

import requests
from bs4 import BeautifulSoup


def gethtml(num):
    url = "https://manhua.fzdm.com/13/"

    response = requests.get(url).text

    soup = BeautifulSoup(response, 'lxml')

    ary = soup.findAll('li', class_='pure-u-1-2 pure-u-lg-1-4')
    ary.reverse()

    for eleindex, ele in enumerate(ary):
        cannext = True
        index = 0

        if eleindex < num:
            continue

        while cannext == True:
            index += 1

            suburl = url + '/' + ele.a.get('href') + '/index_' + str(index) + '.html'
            urlresponse = requests.get(suburl)

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

                with open(dirpath + '/' + str(index) + '.jpg', 'wb') as f:
                    f.write(img)
                    f.close()
                    print(ele.a.get('title') + '  第' + str(index) + '保存成功  ' + 'url= ' + imgurl)


if __name__ == '__main__':
    # 文件太多 经常中断  输入下标 从下标开始爬
    gethtml(0)
