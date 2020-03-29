# -*- coding: utf-8 -*-
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import os
import glob
import time

dir = '/Users/apple/python_project/financial_fyp/data/商业银行年报/'
dir_save_txt = '/Users/apple/python_project/financial_fyp/data/done/'

# os.chdir(dir)

# fp = open('2019-03-29-603993-洛阳钼业：2018年年度报告.PDF', 'rb')
count = 0
number = len(glob.glob(pathname='*.PDF'))
errorList = []

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
number = 0
for item in bank_dictionary:
    # print(item)
    if item[0:2] == '60':
        print(item[0:2])
        print(item[0:3])



#
# for (root, dirs, files) in os.walk(dir):
#     # print(root)
#     # print(dirs)
#     # print(files)
#
#     is_txt_exit = {}
#
#     dir_split_array = root.split('/')
#     year = root.split('/')[-1]
#     url_tmp = dir_save_txt + year
#     print(url_tmp)
#
#     if os.path.exists(url_tmp):
#         for (root_son, dirs_son, files_son) in os.walk(dir_save_txt + year):
#             for file_name_txt in files_son:
#                 if file_name_txt.endswith('.txt') or file_name_txt.endswith('.TXT'):
#                     code = file_name_txt[0:6]
#                     is_txt_exit[code] = True
#         print(is_txt_exit)
#
#     for file in files:
#         if file.endswith('.pdf') or file.endswith('.PDF'):
#             number -= 1
#             code = file[5:11]
#             name = file[12:16]
#             # print(code, ':', '\'', name, '\'')
#             #
#             # if code in bank_dictionary.keys():
#             #     print("=========" + "exit")
#             # else:
#             #     print("===================not exit"+code+':'+name)
