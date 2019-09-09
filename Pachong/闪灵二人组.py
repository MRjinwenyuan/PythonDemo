import multiprocessing
import os
import re
from os import path

import requests
from bs4 import BeautifulSoup


def gethtml(ary):
    url = "https://manhua.fzdm.com/18"
    for  ele in ary:

        cannext = True
        index = 0

        while cannext == True:
            suburl = url + '/' + ele.a.get('href') + 'index_' + str(index) + '.html'
            index += 1

            try:
                #与其两个try不如一次包完
                urlresponse = requests.get(suburl)

                # 中断
                if urlresponse.status_code != 200:
                    cannext = False

                htmlStr = urlresponse.text
                reg = r'(?<=var mhurl1="18/' + ele.a.get('href') + ').*\.jpg'
                imgindex = re.findall(reg, htmlStr)

                dirpath = path.dirname(__file__) + '/闪灵二人组' + '/' + ele.a.get('title')
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)

                if len(imgindex) > 0:
                    imgurl = "http://p0.manhuapan.com/18/" + ele.a.get('href') + imgindex[0]
                    img = requests.get(imgurl).content

                    with open(dirpath + '/' + str(index) + '.jpg', 'wb') as f:
                        f.write(img)
                        f.close()
                        print(ele.a.get('title') + '  第' + str(index) + '保存成功  ' + 'url= ' + imgurl)
            except:
                with open(path.dirname(__file__) + '/闪灵二人组' + '/cuowu.txt', 'a+') as f:
                    f.write(suburl + '\n')
                    f.close()
                continue




def opencuowu():
    list = []

    with open(path.dirname(__file__) + '/闪灵二人组' + '/cuowu.txt', 'r+') as f:
        for row in f:
            list.append(row.strip())

        for ele in list:
            try:
                urlresponse = requests.get(ele)
                htmlStr = urlresponse.text
                reg = r'(?<=var mhurl1="18/).*\.jpg'
                imgindex = re.findall(reg, htmlStr)

                # 正则地址 https://blog.csdn.net/qq_38111015/article/details/80416823

                reg = r'闪灵二人组第.*?卷'
                dirpath = path.dirname(__file__) + '/闪灵二人组' + '/' + re.findall(reg, htmlStr)[0]

                imgurl = "http://p0.manhuapan.com/18/" + imgindex[0]
                img = requests.get(imgurl).content

                reg = r'(?<=卷\(第).*?(?=页)'
                with open(dirpath + '/' + re.findall(reg, htmlStr)[0] + '.jpg', 'wb') as imf:
                    imf.write(img)
                    imf.close()

                # #删除已完成的
                list.remove(ele)
            except Exception as e:
                print(e)

        f.close()

    with open(path.dirname(__file__) + '/闪灵二人组' + '/cuowu.txt', 'w') as f:
        # 重新把失败的写入一次
        for row in list:
            f.write((row + '\n'))
        f.close()


def down():
    url = "https://manhua.fzdm.com/18"
    response = requests.get(url).text

    soup = BeautifulSoup(response, 'lxml')

    ary = soup.findAll('li', class_='pure-u-1-2 pure-u-lg-1-4')

    processNum = 10
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


if __name__ == '__main__':
    down()
    # opencuowu()
