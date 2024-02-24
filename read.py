import numpy as np
'''
未使用到的库
import csv
import math
import matplotlib.pyplot as plt
from scipy.linalg import norm, pinv
'''


def read_csv(csv_name):
    with open(csv_name) as f:
        text = f.readlines()
    i = 0
    n_ex_read = []  # 物品数量集
    c_ex_read = []  # 重量约束集
    z_ex_read = []  # 结果集
    value_ex_read = []  # 价值集
    wei_ex_read = []  # 重量集
    code_ex_read = []  # 答案集

    value_i = np.array([])  # 初始化value_i为numpy数组
    wei_i = np.array([])  # 初始化wei_i为numpy数组
    code_i = np.array([])  # 初始化code_i为numpy数组

    while i < len(text):
        if text[i][0] == 'k':
            # 读取每个问题的开头，共五行，第一行为名称
            ni = float(text[i + 1][2:])  # 第二行为物品数量
            ci = float(text[i + 2][2:])  # 第三行为最大承重
            zi = float(text[i + 3][2:])  # 第四行为最优结果
            # 第五行为运行时间
            n_ex_read.append(ni)  # 将数据添加进n_ex
            c_ex_read.append(ci)  # 将数据添加进c_ex
            z_ex_read.append(zi)  # 将数据添加进z_ex
            value_i = []
            wei_i = []
            code_i = []
            i = i+5  # 跳过五行，开始读取各物品数据
        elif text[i][0] == '-':
            # 除第一个问题，其余问题开头前都由-----隔开
            value_i = np.array(value_i)  # 将读取完后的value_i转化为numpy数组
            wei_i = np.array(wei_i)  # 将读取完后的weii转化为numpy数组
            code_i = np.array(code_i)  # 将读取完后的code_i转化为numpy数组
            value_ex_read.append(value_i)  # 将该问题的value_i加入value_ex中
            wei_ex_read.append(wei_i)  # 将该问题的wei_i加入wei_ex中
            code_ex_read.append(code_i)  # 将该问题的code_i加入code_ex中
            i = i+2  # 跳过两行，开始读取各物品数据

        else:
            # 开始读取数据，利用while循环读取，无需设置循环变量，也不需要知道物品数量即需要循环读取多少次，读完会自动跳转到else if那
            aa = text[i].strip().split(',')  # 读取该行字符串，去掉前后空格并用，分隔
            value_i.append(float(aa[1]))  # 将答案编码添加到value_i末尾
            wei_i.append(float(aa[2]))  # 将答案编码添加到wel_i末尾
            code_i.append(int(aa[3]))  # 将答案编码添加到code_i末尾
            i = i+1  # 跳到下一行

    n_ex_read = np.array(n_ex_read)
    c_ex_read = np.array(c_ex_read)
    z_ex_read = np.array(z_ex_read)
    value_ex_read = np.array(value_ex_read)
    wei_ex_read = np.array(wei_ex_read)
    code_ex_read = np.array(code_ex_read)

    return n_ex_read, c_ex_read, z_ex_read, value_ex_read, wei_ex_read, code_ex_read  # 返回各个值


if __name__ == "__main__":
    n_ex, c_ex, z_ex, value_ex, wei_ex, code_ex = read_csv(r'knapPI_1_50_1000.csv')
