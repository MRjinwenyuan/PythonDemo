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

    try:
        #网络相关的尽量都在 try catch 里面
        title = li.p.string
        onclickstr = li.get("onclick")
        reg = r'(?<=id=).*?(?=\')'
        comicId = re.findall(reg, onclickstr)[0]
        conurl = "http://xs.6taowl.com/index.php?c=commic&a=fetch_chapter&commic_id=" + comicId
        files = {
            'index': (None, 0),
        }
        response = requests.post(url=conurl, headers=headers, files=files).text
        urlindex = response.find("http:\/\/t.xinnwl.com\/www.wzfcyy.cn\/")
        urlstr = response[urlindex:urlindex + 60]
        reg = r'(?<=www.wzfcyy.cn\\/).*?(?=\\/1\\/1.jpg)'
        mhindex = re.findall(reg, urlstr)[0]
    except:
        #这种是一整部没进去
        with open(path.dirname(__file__) + '/韩国漫画' + '/整部错误.txt', 'a+') as f:
            f.write(conurl + '\n')
            f.close()
            return


    conround = 1
    page = 1
    cannext = True

    #写json 的两个中间数组
    imgurls = []
    sumimgs = []
    while cannext == True:
        imgurl = "http://t.xinnwl.com/www.wzfcyy.cn/" + mhindex + "/" + str(conround) + "/" + str(page) + ".jpg"

        try:
            # imgrequest = requests.get(imgurl)
            #写json 用head就行
            imgrequest = requests.head(imgurl)
        except:
            # with open(path.dirname(__file__) + '/韩国漫画' + '/单张错误.txt', 'a+') as f:
            #     f.write( title + '/' +  str(conround) + '/' + str(page) + '.jpg   ' +imgurl + '\n')
            #     f.close()
            #     continue
                continue

        if imgrequest.status_code != 200:
            # 如果第一页都爬不到 那就是这部没有了
            if page == 1:
                cannext = False

            sumimgs.append(imgurls)
            imgurls = []

            conround += 1
            page = 1
            continue

        imgurls.append(imgurl)

        #爬图片代码
        # img = imgrequest.content
        #
        # dirpath = path.dirname(__file__) + '/韩国漫画' + '/' + title + '/' + str(conround)
        #
        # if not os.path.exists(dirpath):
        #     os.makedirs(dirpath)
        #
        # with open(dirpath + '/' + str(page) + '.jpg', 'wb') as f:
        #     f.write(img)
        #     f.close()
        #     print(dirpath + '/' + str(page) + '  保存成功  ' + 'url= ' + imgurl)

        page += 1

    #sumings 就是所有图片数组
    print(sumimgs)

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

    # 已完结的共15页
    for i in range(14):
        url = "http://xs.6taowl.com/index.php?c=commic&a=cates&p=" + str(i + 1) + "&is_finished=2"

        response = requests.get(url=url, headers=headers).text

        soup = BeautifulSoup(response, 'lxml')

        tasklist.extend(soup.findAll('ul', )[3].select('li'))

    # 测试一个
    downfromli(tasklist[0])

    # 下面除了函数参数和时长  其它都不用改变
    # processlist = []
    # processnum = 15
    #
    # for i in range(processnum):
    #     p = multiprocessing.Process(target=funcname, args=(tasklist[0],))
    #     p.start()
    #     processlist.append(p)
    #     tasklist.remove(tasklist[0])
    #
    #
    # while True:
    #     time.sleep(30)
    #     for j in range(processnum):
    #         p = processlist[j]
    #         if p.exitcode != None:
    #
    #             # 没有任务了
    #             if len(tasklist) == 0:return
    #
    #             # 关掉老的P  新建一个P
    #             processlist.remove(p)
    #             p.close()
    #
    #             newp = multiprocessing.Process(target=funcname, args=(tasklist[0],))
    #             newp.start()
    #             processlist.insert(j, newp)
    #             tasklist.remove(tasklist[0])


def opencuowu():
    list = []
    with open(path.dirname(__file__) + '/韩国漫画' + '/单张错误.txt', 'r+') as f:
        for row in f:
            list.append(row.strip())

        for ele in list:
            ary = ele.split("   ", 2)
            imgpath = ary[0]
            imgurl = ary[1]

            imgrequest = requests.get(imgurl).content

            dirpath = path.dirname(__file__) + '/韩国漫画' + '/'

            with open(dirpath + imgpath, 'wb') as f:
                f.write(imgrequest)
                f.close()

                print(dirpath + imgpath)


if __name__ == '__main__':
    pricesspool()
    # opencuowu()
