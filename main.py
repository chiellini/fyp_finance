# -*- coding: utf-8 -*-
import os
import time
import jieba
import xlwt

# dir_pdf_name_checkout = '/Users/apple/python_project/financial_fyp/data/商业银行年报/2018/'

# dir_pdf_name = '/Users/apple/python_project/financial_fyp/data/商业银行年报/2000'
dir_save_txt = '/Users/apple/python_project/financial_fyp/data/done/'

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

word_list = list({'金融科技', '科技金融', '智能', '智慧', '分布式',
                  '数字化', '线上', '电子', '大数据', '互联网',
                  '移动支付', '信用评分', '创新', '云计算',
                  '互联网', 'APP', '风险识别', '区块链',
                  '日活', 'DAU', '量化', '风险监测',
                  '网络金融', '场景化', '个性化', '获客',
                  '生物识别', '供应链', '平台化', '金融生态圈',

                  '第三方支付', '在线支付', '移动支付', '网上支付', '计算机支付', '网络支付',
                  '网上融资', '网上投资', '网贷', '网络融资', '网络投资',
                  '互联网理财', '互联网保险', '在线理财', '网络理财', '网上保险',
                  '互联网渠道', '互联网借贷',
                  '电子银行', '在线银行', '网银', '网上银行', '网络银行',
                  '大数据', '云计算', '人工智能', '人脸识别', '指纹识别',

                  '5G', '5g', '物联网', '虚拟现实', 'VR', 'AR',

                  'IT', '计算机', '互联网技术', '网络', '数字货币',
                  '互联网金融', '科技', '安全', '计算', '底层系统',

                  '虚拟', 'P2P', '手机银行', '掌上', '直销银行', '众筹',
                  # '', '', '', '', '',
                  })


# end


def export_year_excel(files_list, year_self, word_dict, year_dir_root):
    excelbook = xlwt.Workbook()
    sheet = excelbook.add_sheet(year_self + '_word_count')

    sheet.write(0, 0, '名字')
    sheet.write(0, 1, '板块')
    sheet.write(0, 2, '总词数')
    sheet.write(0, 3, '科技词总数')
    # excel 第一行
    for key, value in word_dict.items():
        sheet.write(0, value + 3, key)

    # 文件个数
    file_count = 0
    # 开始处理同一年份的多个文件
    for file_txt in files_list:
        if file_txt.endswith('.txt') or file_txt.endswith('.TXT'):
            # 计算行数
            file_count += 1
            print('dealing with ', year_self, file_txt)
            code = file_txt.split('_')[0]
            sheet.write(file_count, 0, bank_dictionary[code])
            # 所属板块
            if code[0:2] == '60' or code[0:3] == '000':
                sheet.write(file_count, 1, '沪深主板')
            elif code[0:3] == '002':
                sheet.write(file_count, 1, '中小板')
            else:
                sheet.write(file_count, 1, '其他')

            # 打开文件流
            txt = open(os.path.join(year_dir_root, file_txt), 'rb').read()
            words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
            counts = {}  # 通过键值对的形式存储词语及其出现的次数

            for word in words:
                if len(word) == 1:  # 单个词语不计算在内
                    continue
                else:
                    counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

            items = list(counts.items())  # 将键值对转换成列表
            # 根据词语出现的次数进行从大到小排序
            # items.sort(key=lambda x: x[1], reverse=True)

            # 科技类词总数
            all_tech_word_count = 0
            for item in items:
                word, count = item
                if word in word_dict.keys():
                    all_tech_word_count = all_tech_word_count + count
                    print("{0:<5}{1:>5}".format(word, count))
                    sheet.write(file_count, word_dict[word] + 3, count)
            sheet.write(file_count, 2, len(txt))
            sheet.write(file_count, 3, all_tech_word_count)
    target_file = os.path.join(year_dir_root, year_self + '.xls')
    excelbook.save(target_file)


def main():
    word_order_dict = {}
    i_tmp = 0
    word_list.sort(key=lambda x: x[1], reverse=True)

    for word in word_list:
        i_tmp += 1
        word_order_dict[word] = i_tmp

    print(word_order_dict)
    # 遍历所有年份
    for (root, dirs, files) in os.walk(dir_save_txt):
        # is_txt_exit = {}
        # 分割路径，获得文件名
        year = root.split('/')[-1]
        # txt_url_tmp = dir_save_txt + year
        export_year_excel(files, year, word_order_dict, root)


if __name__ == '__main__':
    main()
    # print(__name__)
