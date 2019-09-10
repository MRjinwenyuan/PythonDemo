import multiprocessing
import time


def xiancheng(index):

    print( "进程  " + index + "start")
    time.sleep(10)
    print( "进程  " + index + "end")



def pricesspool():
    # 任务是动态的，有爬到的就新增  开始的就删除
    tasklist = []
    # 函数名
    funcname = xiancheng


    # 下面除了函数参数和时长  其它都不用改变
    processlist = []
    for i in range(20):
        tasklist.append(i)

    processnum = 5

    for i in range(processnum):
        p = multiprocessing.Process(target=funcname, args=(str(tasklist[0]),))
        p.start()
        processlist.append(p)
        tasklist.remove(tasklist[0])


    while True:
        time.sleep(2)
        for j in range(processnum):
            p = processlist[j]
            if p.exitcode != None:

                # 没有任务了
                if len(tasklist) == 0:return

                # 关掉老的P  新建一个P
                processlist.remove(p)
                p.close()

                newp = multiprocessing.Process(target=funcname, args=(str(tasklist[0]),))
                newp.start()
                processlist.insert(j, newp)
                tasklist.remove(tasklist[0])


if __name__ == '__main__':
    pricesspool()