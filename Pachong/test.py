import json
from os import path
import os

if __name__ == '__main__':
    filename = path.dirname(__file__) + '/json/'
    listdir = os.listdir(filename)
    listdir.remove('.DS_Store')
    listdir.remove('目录.txt')

    dic = {"comic": listdir}

    with open(filename + '目录.txt', 'w+') as f:
        json.dump(dic, f)
        f.close()
