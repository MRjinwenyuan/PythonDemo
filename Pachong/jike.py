import requests


def login():
    # formdata = {"country": 86,
    #             "cellphone": "13827418909",
    #             "password": "111111",
    #             "captcha": "",
    #             "remember": 1,
    #             "platform": 3,
    #             "appid": 1}
    #
    # url = "https://account.geekbang.org/account/ticket/login"
    #
    # headers = {
    #     "Host": "account.geekbang.org",
    #     "Connection": "keep-alive",
    #     "Accept": "application/json, text/plain, */*",
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    #     "Sec-Fetch-Mode": "cors",
    #     "Content-Type": "application/json",
    #     "Origin": "https://account.geekbang.org",
    #     "Sec-Fetch-Site": "same-origin",
    #     "Referer": "https://account.geekbang.org/login?mobile=13827418909&redirect=https%3A%2F%2Ftime.geekbang.org%2F",
    #     "Accept-Encoding": " gzip, deflate, br",
    #     "Accept-Language": "zh-CN,zh;q=0.9",
    #     "Cookie": "_ga=GA1.2.1678441281.1566981090; _gid=GA1.2.740185666.1566981090;GCID=dd03455-44860cf-d1db5e3-fc97c3f;_gat=1;SERVERID=3431a294a18c59fc8f5805662e2bd51e|1566981428|1566981090"
    # }
    #
    # response = requests.post(url, data=formdata, headers=headers)
    #
    # print(response.text)

    url = 'http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%CD%BC%C6%AC&fr=ala&ala=1&alatpl=others&pos=0'

    response = requests.get(url).text

    print(response)

if __name__ == '__main__':
    login()
