import pandas as pd
import numpy as np
import os

import math
from numpy import array

dir_save_excel = r'g:\fyp_finance\fyp_finan\data\excel\entropy'

dir_done_excel = r'g:\fyp_finance\fyp_finan\data\excel\bank_blank'

bank_dictionary = {'601577': '长沙银行',
                   '600015': '华夏银行',
                   '002807': '江阴银行',
                   '600908': '无锡银行',
                   '601818': '光大银行',
                   '002948': '青岛银行',
                   '600016': '民生银行',
                   '002958': '青农商行',
                   '601169': '北京银行',
                   '603323': '苏农银行',
                   '601328': '交通银行',
                   '601860': '紫金银行',
                   '600926': '杭州银行',
                   '601166': '兴业银行',
                   '601838': '成都银行',
                   '600919': '江苏银行',
                   '601997': '贵阳银行',
                   '002142': '宁波银行',
                   '002936': '郑州银行',
                   '002839': '张家港行',
                   '601398': '工商银行',
                   '600000': '浦发银行',
                   '601988': '中国银行',
                   '601939': '建设银行',
                   '601009': '南京银行',
                   '601288': '农业银行',
                   '601998': '中信银行',
                   '601229': '上海银行',
                   '600036': '招商银行',
                   '601128': '常熟银行',
                   '600928': '西安银行',
                   '000001': '平安银行'}


def main():
    dict_all_bank_excel = {}
    for value in bank_dictionary:
        dict_all_bank_excel[bank_dictionary[value]] = []

    # print(dict_all_bank_excel)
    os.chdir(dir_save_excel)
    for (root, dirs, files) in os.walk(dir_save_excel):
        for file in files:
            year = file.split('_')[0]
            origin_excel = pd.read_excel(file)

            parser_array = origin_excel.values
            for row_iter in parser_array:
                if row_iter[1] in dict_all_bank_excel.keys():
                    dict_all_bank_excel[row_iter[1]].append(
                        [year, row_iter[2], row_iter[3], row_iter[10] * 1000, row_iter[8]])

                    # parser_excel=origin_excel.drop(columns=origin_excel.columns[0:9])

                    # print(w)
                    # w.index = parser_excel.columns
                    # w.columns = ['weight']
                    #
                    # # print(w.values)
                    # w_array=w.values.reshape((97,))
                    # financial_index = []
                    # origin_array = origin_excel.values
                    # # print(w_array)
                    # count = 0
                    # parser_array = parser_excel.values

                    # print(financial_index)
                    # origin_excel.insert(2,"熵值法指数",financial_index)
                    # print(origin_excel)

                    # origin_excel.to_excel(os.path.join(dir_done_excel, year + 'entropy.xls'))

    for key, value in dict_all_bank_excel.items():
        print("dealing with =====", key, "======document and write in excel")
        print(value)
        df_tmp = pd.DataFrame(data=[], columns=['年份', '板块', '统计指数', '占比指数', '通篇占比'])
        count = 0
        for list_tmp in value:
            df_tmp.loc[count] = list_tmp
            count += 1
        df_tmp.to_excel(os.path.join(dir_done_excel, key + '_bank.xls'))


    
    return


if __name__ == '__main__':
    main()
    # print(__name__)
