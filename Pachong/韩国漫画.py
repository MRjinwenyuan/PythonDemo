import multiprocessing
import os
import re
import time
from os import path

import requests
from bs4 import BeautifulSoup

def downfromli(li):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Cookie': 'PHPSESSID=fvh28283ft5efguovp8cfdmjt1; user=think%3A%7B%22user_id%22%3A%22408436%22%2C%22timestamp%22%3A%221568022564%22%2C%22sign%22%3A%2200070e625217275f999f9b23341a7492%22%7D; Hm_lvt_8b510fc5904051edbfe74a023790a160=1568022568; Hm_lpvt_8b510fc5904051edbfe74a023790a160=1568022568',
        'Content - Disposition': 'form - data',
    }

    title = li.p.string

    onclickstr = li.get("onclick")
    reg = r'(?<=id=).*?(?=\')'
    comicId = re.findall(reg, onclickstr)[0]

    conurl = "http://xs.6taowl.com/index.php?c=commic&a=fetch_chapter&commic_id=" + comicId
    files = {
        'index': (None, 0),
    }

    try:
        response = requests.post(url=conurl, headers=headers, files=files).text
    except:
        #这种是一整部没进去
        with open(path.dirname(__file__) + '/韩国漫画' + '/整部错误.txt', 'a+') as f:
            f.write(conurl + '\n')
            f.close()
            return

    urlindex = response.find("http:\/\/t.xinnwl.com\/www.wzfcyy.cn\/")
    urlstr = response[urlindex:urlindex + 60]
    reg = r'(?<=www.wzfcyy.cn\\/).*?(?=\\/1\\/1.jpg)'
    mhindex = re.findall(reg, urlstr)[0]

    conround = 1
    page = 1
    cannext = True
    while cannext == True:
        imgurl = "http://t.xinnwl.com/www.wzfcyy.cn/" + mhindex + "/" + str(conround) + "/" + str(page) + ".jpg"

        try:
            imgrequest = requests.get(imgurl)
        except:
            with open(path.dirname(__file__) + '/韩国漫画' + '/单张错误.txt', 'a+') as f:
                f.write( title + '/' +  str(conround) + '/' + str(page) + '.jpg   ' +imgurl + '\n')
                f.close()
                continue

        if imgrequest.status_code != 200:
            # 如果第一页都爬不到 那就是这部没有了
            if page == 1:
                cannext = False

            conround += 1
            page = 1
            continue

        img = imgrequest.content

        dirpath = path.dirname(__file__) + '/韩国漫画' + '/' + title + '/' + str(conround)

        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        with open(dirpath + '/' + str(page) + '.jpg', 'wb') as f:
            f.write(img)
            f.close()
            print(dirpath + '/' + str(page) + '  保存成功  ' + 'url= ' + imgurl)

        page += 1

def pricesspool():
    # 任务是动态的，有爬到的就新增  开始的就删除
    tasklist = []
    # 函数名
    funcname = downfromli

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Cookie': 'PHPSESSID=fvh28283ft5efguovp8cfdmjt1; user=think%3A%7B%22user_id%22%3A%22408436%22%2C%22timestamp%22%3A%221568022564%22%2C%22sign%22%3A%2200070e625217275f999f9b23341a7492%22%7D; Hm_lvt_8b510fc5904051edbfe74a023790a160=1568022568; Hm_lpvt_8b510fc5904051edbfe74a023790a160=1568022568',
        'Content - Disposition': 'form - data',
    }

    # 完结的 15页
    for i in range(14):
        url = "http://xs.6taowl.com/index.php?c=commic&a=cates&p=" + str(i + 1) + "&is_finished=2"

        response = requests.get(url=url, headers=headers).text

        soup = BeautifulSoup(response, 'lxml')

        tasklist.extend(soup.findAll('ul', )[3].select('li'))

    # 下面除了函数参数和时长  其它都不用改变
    processlist = []
    processnum = 3

    for i in range(processnum):
        p = multiprocessing.Process(target=funcname, args=(tasklist[0],))
        p.start()
        processlist.append(p)
        tasklist.remove(tasklist[0])


    while True:
        time.sleep(30)
        for j in range(processnum):
            p = processlist[j]
            if p.exitcode != None:

                # 没有任务了
                if len(tasklist) == 0:return

                # 关掉老的P  新建一个P
                processlist.remove(p)
                p.close()

                newp = multiprocessing.Process(target=funcname, args=(tasklist[0],))
                newp.start()
                processlist.insert(j, newp)
                tasklist.remove(tasklist[0])

if __name__ == '__main__':
    pricesspool()
