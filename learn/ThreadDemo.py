# -*- coding: utf-8 -*-
def mathDef(x):
    ret=1;
    if x is not None:
        for i in range(len(x)):
            ret*=x[i]
    return ret;
def poolDef():
    from multiprocessing import Pool
    data_list=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)]
    with Pool(5) as p:
        print(p.map(mathDef,data_list))
def info(title):
    import os
    print(title)
    print('module name:', __name__)# 返回文件名
    print('parent process:', os.getppid())# 返回父进程PID
    print('process id:', os.getpid())# 返回当前进程的PID

def f(name):
    info('function f')
    print('hello', name)

def processDef():
    from multiprocessing import Process
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
def foo(q):
    q.put('hello')
def spawnDef():
    import multiprocessing as mp
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()

def f(q):
    q.put([42, None, 'hello'])
def processQueue():
    from multiprocessing import Process, Queue
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()

def fl(conn):
    conn.send([42, None, 'hello'])
    conn.close()
def processPipe():
    from multiprocessing import Process, Pipe
    parent_conn, child_conn = Pipe()
    p = Process(target=fl, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()

def fs(n,a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]
def memoryDef():
    from multiprocessing import Process, Value, Array
    num = Value('d', 0.0)
    arr = Array('i', range(5))
    p = Process(target=fs, args=(num, arr))
    p.start()
    p.join()

    print(num.value)# 3.1415927
    print(arr[:])# [0, -1, -2, -3, -4]
    # 创建 num 和 arr 时使用的 'd' 和 'i' 参数是 array 模块使用的类型的 typecode ： 'd' 表示双精度浮点数， 'i' 表示有符号整数。这些共享对象将是进程和线程安全的。

def fq(d,l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()
def managerDef():
    from multiprocessing import Process, Manager
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))
        p = Process(target=fq, args=(d, l))
        p.start()
        p.join()
        print(d)# {1: '1', '2': 2, 0.25: None}
        print(l)# [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

def flast(x):
    return x*x;
def poolFun():
    from multiprocessing import Pool, TimeoutError
    import time
    import os
    # start 4 worker processes
    with Pool(processes=40) as pool:
        # print "[0, 1, 4]"
        print(pool.map(flast, range(30)))
        # print same numbers in arbitrary order
        for i in pool.imap_unordered(flast, range(30)):
            print(i)# 0 1 4
        # 异步评估flats(20)
        res = pool.apply_async(flast, (20,))      # runs in *only* one process
        print(res.get(timeout=1))             # prints "400"
        # 异步评估os.getpid
        res = pool.apply_async(os.getpid, ()) # runs in *only* one process
        print(res.get(timeout=1))             # prints the PID of that process
        # 异步地启动多个计算可能会使用更多的进程
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(40)]
        print([res.get(timeout=1) for res in multiple_results])
        # 让一个进程休息10ms
        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")
        print("For the moment, the pool remains available for more work")
    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")
def runThread():
    # poolDef();
    # processDef();
    # spawnDef();
    # processQueue();
    # processPipe();
    # memoryDef();
    # managerDef();
    poolFun();