#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: drawResults.py
# @time: 2020/10/30 0030 9:22
# @desc:

import matplotlib.pyplot as plt
import numpy as np
import xlrd
from utils.pfget import get_pflist

def read_excel(fname):
    # 打开文件
    workBook = xlrd.open_workbook(fname)
    hvs = []
    igds = []
    for i in range(7):
        sheet = workBook.sheet_by_index(i) # sheet索引从0开始
        hvs.append(sheet.row_values(1)[1:11])
        igds.append(sheet.row_values(2)[1:11])
    return hvs, igds
    # # 5. 获取单元格内容(三种方式)
    # print(sheet1_content1.cell(1, 0).value)
    # print(sheet1_content1.cell_value(2, 2))
    # print(sheet1_content1.row(2)[2].value)
    #
    # # 6. 获取单元格内容的数据类型
    # # Tips: python读取excel中单元格的内容返回的有5种类型 [0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error]
    # print(sheet1_content1.cell(1, 0).ctype)


def draw_box(data, name, png_name):
    '''
    根据数据画盒图
    :param data:
    :return:
    '''
    plt.figure()
    plt.boxplot(data, notch=False, sym='o', vert=True)
    plt.xticks([1,2, 3,4],['MOEA/D', 'MOEA/D-DE', 'MOEA/D-SaDE', 'MOEA/D-CoDE'])
    plt.title(name)
    plt.savefig(png_name)
    plt.close()
    # plt.show()

def draw_box2(res):
    '''
    对四个算法模型、16个benchmark计算结果进行画图
    '''
    name = ['DTLZ1','DTLZ2','DTLZ3','DTLZ4','DTLZ5','DTLZ6','DTLZ7',
            'WFG1','WFG2','WFG3','WFG4','WFG5','WFG6','WFG7','WFG8','WFG9']
    for i in range(16):
        hvs = [res[0][name[i]][0], res[1][name[i]][0], res[2][name[i]][0], res[3][name[i]][0]]
        draw_box(hvs, name[i]+' HV')
        igds = [res[0][name[i]][1], res[1][name[i]][1], res[2][name[i]][1], res[3][name[i]][1]]
        draw_box(igds, name[i]+' IGD')



if __name__ == '__main__':
    pass
    # hvs, igds = read_excel('../results/excels/moead.xls')
    # hvs1, igds1 = read_excel('../results/excels/moeadde.xls')
    # hvs2, igds2 = read_excel('../results/excels/moeadcode.xls')
    # hvs3, igds3 = read_excel('../results/excels/moeadsade.xls')
    # for i in range(7):
    #     data = [hvs[i],hvs1[i], hvs2[i], hvs3[i]]
    #     draw_box(data, 'DTLZ{} HV results in ten times'.format(i+1))
    #
    #     data_igd = [igds[i], igds1[i], igds2[i], igds3[i]]
    #     draw_box(data_igd, 'DTLZ{} IGD results in ten times'.format(i+1))

