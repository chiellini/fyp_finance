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

dir_pdf_name_checkout = '/Users/apple/python_project/financial_fyp/data/商业银行年报/2018/'
dir_save_txt = '/Users/apple/python_project/financial_fyp/data/done/2018/'

bank_dictionary = {}
is_txt_exit = {}
number = 0

os.chdir(dir_pdf_name_checkout)
for (root, dirs, files) in os.walk(dir_pdf_name_checkout):
    print(files)
    for file_pdf in files:
        if file_pdf.endswith('.pdf') or file_pdf.endswith('.PDF'):
            number += 1
            code = file_pdf[11:17]
            name = file_pdf[18:22]
            bank_dictionary[code] = name
            is_txt_exit[code] = 0


# check if txt exit
# os.chdir(dir_pdf_name_checkout)
for (root, dirs, files) in os.walk(dir_save_txt):
    for file_name_txt in files:
        if file_name_txt.endswith('.txt') or file_name_txt.endswith('.TXT'):
            code = file_name_txt[0:6]
            is_txt_exit[code] = is_txt_exit[code] + 1

print(number)

# https://www.cnblogs.com/jamespei/p/5339769.html
# https://www.cnblogs.com/jamespei/p/5339769.html
for (root, dirs, files) in os.walk(dir_pdf_name_checkout):
    for file_pdf in files:
        print(file_pdf)
        if file_pdf.endswith('.pdf') or file_pdf.endswith('.PDF'):
            number -= 1
            code = file_pdf[11:17]

            if bank_dictionary[code] and is_txt_exit[code] == 0:
                print('start processing ', code, ';', str(number), 'files left.')
                time_start = time.time()
                fp = open(file_pdf, 'rb')
                # 来创建一个pdf文档分析器，用来提取数据
                parser = PDFParser(fp)
                # 创建一个PDF文档对象存储文档结构，用来在内存中保存数据
                document = PDFDocument(parser)
                # 检查文件是否允许文本提取

                # os.renames(os.path.join(dir_pdf_name, file_pdf), os.path.join(dir_pdf_name, code + '.pdf'))
                if not document.is_extractable:
                    print(file_pdf)
                    print(code)
                    print('==========fail to extract==========', str(code), ':', bank_dictionary[code])
                    raise PDFTextExtractionNotAllowed
                    continue
                else:
                    # 创建一个PDF资源管理器对象来保存共享内容，如字体和图片
                    rsrcmgr = PDFResourceManager()

                    # 设定参数进行分析
                    laparams = LAParams()
                    # 创建一个PDF设备对象
                    # device=PDFDevice(rsrcmgr)
                    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                    # 创建一个PDF解释器对象
                    interpreter = PDFPageInterpreter(rsrcmgr, device)
                    # 处理每一页
                    pageCount = 0

                    for page in PDFPage.create_pages(document):
                        pageCount += 1
                        # 从第5页开始
                        if pageCount > 5:
                            print('processing page' + str(pageCount))
                            interpreter.process_page(page)
                            # 接受该页面的LTPage对象
                            layout = device.get_result()
                            for x in layout:
                                # 这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
                                # 一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
                                # 想要获取文本就得获取对象的text属性

                                if isinstance(x, LTTextBoxHorizontal):
                                    text = x.get_text()
                                    # if '经营情况讨论与分析' in text:
                                    #     printFlag = True
                                    # if printFlag:
                                    with open(
                                            dir_save_txt + code + '_' +
                                            bank_dictionary[code] + '.txt',
                                            'a') as f:
                                        f.write(x.get_text())
                                # if '重要事项' in text:
                                #     readFlag = False
                                #     break
                    # if readFlag is False:
                    #     break
                time_end = time.time()
                print('time cost for ', code, 'is', time_end - time_start, 's')
