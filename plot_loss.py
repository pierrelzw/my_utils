#!/usr/bin/env python
#--code: utf-8 --
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import re
import pylab
from pylab import figure, show, legend
from mpl_toolkits.axes_grid1 import host_subplot

log_file = sys.argv[1]
max_iter = int(sys.argv[2])

save_path = log_file + '_' + str(max_iter)+"_loss.png"

if os.path.exists(save_path):
	print("target loss img exists, stop plotting.")
else: 
    print("open log file: %s"%log_file)
    fp = open(log_file, 'r')#, encoding='UTF-8')
    train_iterations = []
    train_loss = []
    test_iterations = []
    #test_accuracy = []
    loss_bbox = []
    loss_cls = []
    rpn_cls_loss = []
    rpn_loss_bbox = []
    for i,ln in enumerate(fp):
        # print(i)
        # get train_iterations and train_loss
        if '] Iteration ' in ln and 'loss = ' in ln:
            arr = re.findall(r'ion \b\d+\b,',ln)
            train_iterations.append(int(arr[0].strip(',')[4:]))
            train_loss.append(float(ln.strip().split(' = ')[-1]))
            # print('loss')
            continue
        if ' loss_bbox = ' in ln:
            loss_bbox.append(float(ln.split('loss_bbox = ')[1].strip().split('(')[0].strip()))
            # print('loss_bbox')
            continue
        if ' loss_cls = ' in ln:
            loss_cls.append(float(ln.split('loss_cls = ')[1].strip().split('(')[0].strip())) 
            # print('loss_cls')
            continue
        if ' rpn_cls_loss = ' in ln:
            rpn_cls_loss.append(float(ln.split('rpn_cls_loss = ')[1].strip().split('(')[0].strip())) 
            # print('rpn_cls_loss')
            continue
        if ' rpn_loss_bbox = ' in ln:
            rpn_loss_bbox.append(float(ln.split('rpn_loss_bbox = ')[1].strip().split('(')[0].strip()))
            # print('rpn_loss_bbox')
            continue
    fp.close()
    print(len(train_iterations))
    print(len(train_loss))

    print(len(loss_bbox))
    print(len(loss_cls))
    print(len(rpn_cls_loss))
    print(len(rpn_loss_bbox))
    # a = input()

    fig = plt.figure(figsize=[8,4])
    plt.rcParams['savefig.dpi'] = 300 #
    plt.rcParams['figure.dpi'] = 100 #
    host1 = host_subplot(111)
    plt.subplots_adjust(right=0.8) # ajust the right boundary of the plot window
    #par1 = host.twinx()
    # set labels
    host1.set_xlabel("iterations")
    host1.set_ylabel("RPN loss")
    #par1.set_ylabel("validation accuracy")

    # plot curves
    p1, = host1.plot(train_iterations, train_loss, label="train RPN loss")

    host1.legend(loc=1)
    # set label color
    host1.axis["left"].label.set_color(p1.get_color())
    host1.set_xlim([-1000, max_iter])
    host1.set_ylim([0., 3.5])
    plt.show()
    fig.savefig(save_path)

    fig = plt.figure(figsize=[8,4])
    save_path = log_file + '_' + str(max_iter)+"_loss_bbox.png"
    
    host2 = host_subplot(111)
    host2.set_ylabel("loss_bbox")
    host2.plot(train_iterations, loss_bbox)
    plt.show()
    fig.savefig(save_path)

    fig = plt.figure(figsize=[8,4])
    save_path = log_file + '_' + str(max_iter)+"_loss_cls.png"
    host3 = host_subplot(111)
    host3.set_ylabel("loss_cls")
    host3.plot(train_iterations, loss_cls)
    plt.show()
    fig.savefig(save_path)
	
    fig = plt.figure(figsize=[8,4])
    save_path = log_file + '_' + str(max_iter)+"_rpn_cls_loss.png"
    host4 = host_subplot(111)
    host4.set_ylabel("rpn_cls_loss")
    host4.plot(train_iterations, rpn_cls_loss)
    plt.show()
    fig.savefig(save_path)

    fig = plt.figure(figsize=[8,4])
    save_path = log_file + '_' + str(max_iter)+"_rpn_loss_bbox.png"
    host5 = host_subplot(111)
    host5.set_ylabel("rpn_loss_bbox")
    host5.plot(train_iterations, rpn_loss_bbox)
    plt.show()
    fig.savefig(save_path)

    # plt.draw()
    plt.show()
    # fig.savefig(save_path)