import pandas as pd
import numpy as np
import os

import math
from numpy import array

dir_save_excel = r'g:\fyp_finance\fyp_finan\data\excel\synthesize'

dir_done_excel = r'g:\fyp_finance\fyp_finan\data\excel\entropy_1'

dir_done_excel_all = r'g:\fyp_finance\fyp_finan\data\excel'

data_class = [['金融科技',
               '科技金融',
               '创新',
               '网络金融',
               '金融生态圈',
               '智能',
               '智慧',
               '互联网金融',
               'Fintech',
               '网络化',
               '数据化',
               '智能化',
               '电子',
               ],
              ['线上',
               '互联网',
               'APP',
               '日活',
               'DAU',
               '手机',
               '网银',
               '互联网渠道',
               '电子银行',
               '在线银行',
               '手机银行',
               '网络',
               '掌上',
               '智能设备',
               '网上银行',
               '网络银行',
               '直销银行'],
              ['移动支付',
               '第三方支付',
               '在线支付',
               '网上支付',
               '计算机支付',
               '网络支付',
               '数字货币',
               '电子账单'
               ],
              ['场景化',
               '个性化',
               '获客',
               '风险识别',
               '风险监测',
               '移动应用',
               '互联',
               '电商',
               'e融',
               'E融',
               '平台化',
               '信用评分',
               '供应链'
               ],
              ['网上投资',
               '网贷',
               '网络融资',
               '网络投资',
               '互联网理财',
               '互联网保险',
               '在线理财',
               '网络理财',
               '网上保险',
               '互联网借贷',
               'P2P',
               '众筹',
               '智投',
               '网上融资'
               ],
              [
                  '分布式',
                  '数字化',
                  '大数据',
                  '云计算',
                  '区块链',
                  '量化',
                  '生物识别',
                  '人工智能',
                  '人脸识别',
                  '指纹识别',
                  '物联网',
                  '虚拟现实',
                  'IT',
                  '互联网技术',
                  '计算机',
                  '科技',
                  '计算',
                  '底层系统',
                  '虚拟',
                  'O2O',
                  '机器',
                  '云',
                  '信息技术',
                  '研发',
                  '数据',
                  '5G',
                  '5g',
                  'VR',
                  'AR'

              ]]

year_class_analysis = {}


def cal_weight(x):
    '''熵值法计算变量的权重'''
    # 标准化
    x = x.apply(lambda x: ((x - np.min(x)) / (np.max(x) - np.min(x))))

    # 求k
    rows = x.index.size  # 行
    cols = x.columns.size  # 列
    #
    if rows == 0:
        return pd.DataFrame([[0] * 1 for i in range(cols)])
    elif math.log(rows) == 0:
        return pd.DataFrame([[0] * 1 for i in range(cols)])

    else:
        k = 1.0 / math.log(rows)

    # lnf = [[None] * cols for i in range(rows)]

    # 矩阵计算--
    # 信息熵
    # p=array(p)
    x = array(x)
    lnf = [[None] * cols for i in range(rows)]
    lnf = array(lnf)
    # print(lnf)

    for i in range(0, rows):
        for j in range(0, cols):
            if x[i][j] == 0:
                lnfij = 0.0
            else:
                p = x[i][j] / x.sum(axis=0)[j]
                lnfij = math.log(p) * p * (-k)
            lnf[i][j] = lnfij
    lnf = pd.DataFrame(lnf)
    E = lnf
    # print(lnf)
    # 计算冗余度
    d = 1 - E.sum(axis=0)
    # 计算各指标的权重
    w = [[None] * 1 for i in range(cols)]
    for j in range(0, cols):
        wj = d[j] / sum(d)
        w[j] = wj
        # 计算各样本的综合得分,用最原始的数据

    w = pd.DataFrame(w)
    return w


def main():
    os.chdir(dir_save_excel)
    for (root, dirs, files) in os.walk(dir_save_excel):
        for file in files:

            year = file.split('_')[0]
            print("dealing with =====", year, "======document and write in excel")
            origin_excel = pd.read_excel(file)
            origin_excel.dropna()

            parser_excel = origin_excel.drop(columns=origin_excel.columns[0:9])
            # print(parser_excel.index.values)
            w = cal_weight(parser_excel)

            w.index = parser_excel.columns
            w.columns = ['weight']
            # print(w.loc['金融科技','weight'])
            w_array = w.values.reshape((97,))
            financial_index = []
            origin_array = origin_excel.values
            count = 0
            parser_array = parser_excel.values
            for row_iter in parser_array:
                # print(row_iter)
                count_after = np.dot(row_iter, w_array.T)
                financial_index.append((count_after*100) ** 2 / origin_array[count, 3])
                count += 1
            # print(financial_index)
            origin_excel.insert(2, "熵值法指数", financial_index)

            supply_ndarray = np.zeros((10,))
            # print(supply_ndarray)
            w_array = np.append(supply_ndarray, w_array)
            # df_tmp=pd.DataFrame(columns=origin_excel.columns)
            # print(w_array)
            #origin_excel.loc[len(origin_excel)] = list(w_array)
            # origin_excel.loc[len(origin_excel)] = list((1 / w_array) / 1000)

            class_count = [0, 0, 0, 0, 0, 0]
            class_analysis = {}
            # 计算每一类的值
            for row_index, row_ in enumerate(data_class):
                # print(type(row_index))
                for column_index, column_ in enumerate(data_class[row_index]):
                    class_count[row_index] += w.loc[data_class[row_index][column_index], 'weight']

            class_analysis['重视程度'] = class_count[0]
            class_analysis['构筑渠道'] = class_count[1]
            class_analysis['支付清算'] = class_count[2]
            class_analysis['场景应用'] = class_count[3]
            class_analysis['财富管理'] = class_count[4]
            class_analysis['技术支持'] = class_count[5]
            year_class_analysis[year] = class_analysis

            # origin_excel.loc[len(origin_excel)]=list(class_analysis)

            origin_excel.to_excel(os.path.join(dir_done_excel, year + '_entropy.xls'))
            # excelbook = xlwt.Workbook()
            # sheet = excelbook.add_sheet(year_self + '_count')
            #
            # target_file = os.path.join(dir_save_excel, year_self + '_synthesis_word.xls')
            # excelbook.save(target_file)

    df = pd.DataFrame(columns=['重视程度', '构筑渠道', '支付清算', '场景应用', '财富管理', '技术支持'])
    for key in year_class_analysis.keys():
        df.loc[key] = year_class_analysis[key]
    print(df)
    df.to_excel(os.path.join(dir_done_excel_all, 'all_year_entropy_index_1.xls'))

    return


if __name__ == '__main__':
    main()
    # print(__name__)
