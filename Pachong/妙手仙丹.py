from os import path
import os

import requests
from bs4 import BeautifulSoup


def gethtml(num):
    url = "https://www.mkzhan.com/210400"
    response = requests.get(url).text

    soup = BeautifulSoup(response, 'lxml')

    ary = soup.findAll('a', class_='j-chapter-link')
    # 逆序
    ary.reverse()

    for index,ele in enumerate(ary):
        if index < num:
            continue

        suburl = "https://www.mkzhan.com/210400/" + ele.get('data-chapterid') + ".html"
        subresponse = requests.get(suburl).text
        subsoup = BeautifulSoup(subresponse, 'lxml')
        imgurls = subsoup.findAll('img', class_="lazy-read")
        dirpath = path.dirname(__file__) + '/妙手仙丹' + '/' + '第' + str(index) + '话'
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        for i, img in enumerate(imgurls):
            with open(dirpath + '/' + str(i) + '.jpg', 'wb') as f:
                imgdata = requests.get(img.get("data-src")).content
                f.write(imgdata)
                f.close()


if __name__ == '__main__':
    gethtml(134)

