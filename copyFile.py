# -*- coding: utf-8 -*-
from multiprocessing import Pool,Manager
import time
import os
import shutil
import random

#从源文件夹复制到目标文件夹
def copyFile(file_name, old_folder_name, new_folder_name, q):
    time.sleep(random.random())
    shutil.copyfile(old_folder_name + "/" + file_name, new_folder_name + "/" + file_name,)
    q.put(file_name)

def copyDir(old_folder_name, new_folder_name):
    start = time.time()
    #创建 Ｐｏｏｌ
    pool = Pool(5)
    #创建小心队列
    q = Manager().Queue()

    #获取待拷贝的文件夹名
    #old_folder_name = input("请输入你要拷贝的文件夹名称：")

    #组装目标文件夹名称
    #new_folder_name = old_folder_name + "-复制"
    if not os.path.exists(new_folder_name):
        os.mkdir(new_folder_name)

    file_name_list = os.listdir(old_folder_name)

    for value in file_name_list:
        pool.apply_async(copyFile, args=(value, old_folder_name, new_folder_name, q))

    count = 0
    allLength = len(file_name_list)
    while count < allLength:
        message = q.get()
        count += 1
        print("\r正在拷贝%s, 拷贝的进度是:%d%%"%(message, (count/allLength)*100), end="")

    print("\n拷贝完毕")
    end = time.time()
    print("多进程花费的时间：%#.2fs"%(end-start))
def main():
    pass
if __name__ == "__main__":
    main()
