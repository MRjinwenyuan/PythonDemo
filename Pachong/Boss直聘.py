import pymysql
import requests


def linkSQL():
    coon = pymysql.connect('localhost', 'root', '12345678', '')
    cursor = coon.cursor()


def gethtml():
    header: {
        'authority': 'www.zhipin.com',

    }

    url = "https://www.zhipin.com/c101280600-p100203/?page=1&ka=page-1"

    response = requests.get(url).text
    print(response)


if __name__ == '__main__':
    # linkSQL()
    gethtml()
