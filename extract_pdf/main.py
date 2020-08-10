# -*- coding: utf-8 -*-
from wand.image import Image
from PIL import Image as PI
import io
import pyocr
import pyocr.builders

import os
import glob
import time
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
from multiprocessing import Process
import winshell

tmp_folder = r'C:\Users\chiellini\AppData\Local\Temp'


# tmp_folder='G:\\\\fyp_finance\\fyp_finan\\data\\tmp_folder'

def clear_tmp_trash_path():
    os.chdir(tmp_folder)
    # clear temp folder otherwise my disk C will boom
    for (root_tmp, dirs_tmp, files_tmp) in os.walk(tmp_folder):
        for file_name_tmp in files_tmp:
            file_path_tmp_ = os.path.join(tmp_folder, file_name_tmp)
            if file_path_tmp_.startswith("magick-") or file_path_tmp_.endswith('.jpg'):
                try:
                    os.remove(file_path_tmp_)
                except:
                    print('remove ', file_path_tmp_)


def PYOCR(filename_, saving_path):
    # for (root_tmp, dirs_tmp, files_tmp) in os.walk(tmp_folder):
    #     for file_name_tmp in files_tmp:
    #         file_path_tmp_ = os.path.join(tmp_folder, file_name_tmp)
    #         # print(file_name_tmp[0:6])
    #         if os.path.isfile(file_path_tmp_) and file_name_tmp[0:6] == 'magick':
    #             os.remove(file_path_tmp_)
    # # os.chdir('C:\\\\Users\\chiellini')
    cache = os.listdir(tmp_folder)

    # winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)

    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0]

    req_image = []
    final_text = []
    print(tool.get_available_languages())
    print(lang)

    file_name = filename_
    print('deal with, magick')
    image_pdf = Image(filename=file_name, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')

    # start_time
    count = 0
    for img in image_jpeg.sequence:
        count += 1
        print("dealing with ", count, 'with wand')
        image_page = Image(image=img)
        image_page.type = 'grayscale'
        req_image.append(image_page.make_blob('jpeg'))
        # print("dealing with ", count, 'with tesseract')

    count = 0
    for img in req_image:
        count += 1
        print("dealing with ", count, 'with PYOCR')
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        with open(
                saving_path,
                'a') as f:
            f.write(txt)

    for item in cache:
        if item.endswith(".jpg") or item.startswith("magick-"):
            try:
                os.remove(os.path.join(tmp_folder, item))
            except:
                print('delete failed ', os.path.join(tmp_folder, item))

    # # clear temp folder otherwise my disk C will boom

    # print('delete', file_path_tmp_)

    # print('delete', file_path_tmp_)
    # elif os.path.isdir(file_path_tmp_):
    #     os.removedirs(file_path_tmp_)
    #     # print('delete', file_path_tmp_)


def main():
    # dir_pdf_name_checkout = '/Users/apple/python_project/financial_fyp/data/商业银行年报/2018/'

    dir_pdf_name = r'g:\fyp_finance\fyp_finan\data\yea_report'
    dir_save_txt = r'g:\fyp_finance\fyp_finan\data\done'

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

    # os.chdir(dir_pdf_name)

    # https://www.cnblogs.com/jamespei/p/5339769.html
    for (root, dirs, files) in os.walk(dir_pdf_name):

        is_txt_exit = {}
        year = os.path.split(root)[-1]

        txt_url_tmp = os.path.join(dir_save_txt, year)

        print(txt_url_tmp)

        if os.path.exists(txt_url_tmp):
            for (root_son, dirs_son, files_son) in os.walk(txt_url_tmp):
                for file_name_txt in files_son:
                    print(file_name_txt)
                    if file_name_txt.endswith('.txt') or file_name_txt.endswith('.TXT'):
                        code = file_name_txt[0:6]

                        is_txt_exit[code] = True
        else:
            os.mkdir(txt_url_tmp)

        for file_pdf in files:
            # print(file_pdf)
            if file_pdf.endswith('.pdf') or file_pdf.endswith('.PDF'):

                code = file_pdf[5:11]

                if code in bank_dictionary.keys() and code not in is_txt_exit.keys():
                    number += 1
                    print('start processing ', code, file_pdf, '; NO.', str(number), 'files.')
                    time_start = time.time()
                    fp = open(os.path.join(dir_pdf_name, year, file_pdf), 'rb')
                    # 来创建一个pdf文档分析器，用来提取数据
                    parser = PDFParser(fp)
                    # 创建一个PDF文档对象存储文档结构，用来在内存中保存数据
                    document = PDFDocument(parser)
                    # 检查文件是否允许文本提取

                    # os.renames(os.path.join(dir_pdf_name, file_pdf), os.path.join(dir_pdf_name, code + '.pdf'))
                    if not document.is_extractable:
                        print(file_pdf)
                        print(code)
                        print('==========fail to extract, use OCR==========', str(code), ':', bank_dictionary[code])
                        clear_tmp_trash_path()
                        PYOCR(os.path.join(dir_pdf_name, year, file_pdf),
                              os.path.join(txt_url_tmp, code + '_' + bank_dictionary[code] + '.txt'))
                       # raise PDFTextExtractionNotAllowed
                        # continue
                    else:
                        print('============================================no txt and can use pdfminer =============')
                        # continue
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
                            if pageCount > 10:
                                # 从第10页开始
                                interpreter.process_page(page)
                                # 接受该页面的LTPage对象
                                layout = device.get_result()
                                for x in layout:
                                    # 这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
                                    # 一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
                                    # 想要获取文本就得获取对象的text属性

                                    if isinstance(x, LTTextBoxHorizontal):
                                        # text = x.get_text()

                                        with open(
                                                os.path.join(txt_url_tmp, code + '_' + bank_dictionary[code] + '.txt'),
                                                'a',
                                                errors='ignore'
                                        ) as f:
                                            f.write(x.get_text())
                        # # if readFlag is False:
                        # #     break
                    time_end = time.time()
                    print('time cost for ', code, bank_dictionary[code], 'is', time_end - time_start, ' s')


if __name__ == '__main__':
    main()
    # print(__name__)
