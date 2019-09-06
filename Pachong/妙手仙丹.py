import multiprocessing
from os import path
import os
import requests
from bs4 import BeautifulSoup


def gethtml(ary):
    for ele in ary:
        suburl = "https://www.mkzhan.com/210400/" + ele.get('data-chapterid') + ".html"
        subresponse = requests.get(suburl).text
        subsoup = BeautifulSoup(subresponse, 'lxml')
        imgurls = subsoup.findAll('img', class_="lazy-read")

        dirpath = path.dirname(__file__) + '/妙手仙丹' + '/' + subsoup.title.string
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        for i, img in enumerate(imgurls):
            with open(dirpath + '/' + str(i) + '.jpg', 'wb') as f:
                imgdata = requests.get(img.get("data-src")).content
                f.write(imgdata)
                f.close()
                print('/妙手仙丹' + '/' + subsoup.title.string + '保存成功  ' + 'url= ' + img.get("data-src"))


if __name__ == '__main__':

    url = "https://www.mkzhan.com/210400"
    response = requests.get(url).text

    soup = BeautifulSoup(response, 'lxml')

    ary = soup.findAll('a', class_='j-chapter-link')
    # 逆序
    # ary.reverse()

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
