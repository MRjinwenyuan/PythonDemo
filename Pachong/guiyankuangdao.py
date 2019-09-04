import random
from os import path

import requests
from bs4 import BeautifulSoup
import re

def gethtml():

    url = "https://manhua.fzdm.com/13/"

    response = requests.get(url).text

    soup = BeautifulSoup(response,'lxml')

    ary = soup.findAll('li',class_='pure-u-1-2 pure-u-lg-1-4')
    # print(ary[0].a.get('href'))
    # print(ary[0].a.get('title'))

    # cannext = True
    # index = 0
    #
    # while cannext == True:
    #     index += 1
    #     print(index)
    #
    #     headers = {
    #         'Connection': 'close'
    #     }
    #
    #     user_agent_list = [
    #         "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    #         "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    #         "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
    #         "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    #         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    #         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    #         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    #         "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    #         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    #         "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    #         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    #         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
    #         "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
    #         "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
    #         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    #         "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
    #         "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
    #         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
    #         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    #         "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0",
    #         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
    #         "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
    #         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201",
    #         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    #         ]
    #     headers['User-Agent'] = random.choice(user_agent_list)
    #
    #     suburl = 'https://manhua.fzdm.com/13/'+ary[0].a.get('href')+'/index_'+str(index)+'.html'
    #     urlresponse = requests.get(suburl,headers=headers)
    #
    #     #中断
    #     if urlresponse.status_code != 200:
    #         cannext = False
    #
    #     htmlStr = urlresponse.text
    #     reg = r'(?<=var mhurl1="13/'+ary[0].a.get('href')+').*\.jpg'
    #     imgindex = re.findall(reg,htmlStr)
    #
    #     if len(imgindex) > 0:
    #         imgurl = "http://p0.manhuapan.com/13/" + ary[0].a.get('href') + imgindex[0]
    #         img = requests.get(imgurl).content
    #
    #         with open(path.dirname(__file__) + '/manhua/' + str(index) + '.jpg', 'wb') as f:
    #             f.write(img)
    #             f.close()
    #             print(str(index)+ '保存成功  ' + 'url= ' + imgurl)

    for ele in ary:
        print(ele)


if __name__ == '__main__':
    gethtml()