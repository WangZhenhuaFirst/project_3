# _*_ coding utf-8 _*_
'''
观察PDF2htmlEX程序处理PDF文件生成的HTML代码发现：
1， 文本内容全部存在于<page-container>标签下的子标签内
2， <page-container>标签下的每一页PDF文件单独存在于一个<div>标签模块内
3， 每一页<div>下的文本，按行为模块，存为一个<div>子标签，此子标签内存放文本内容
4， 但是文本内容被大量<span></span>空格标签隔开
思路：
1， 正则化去除HTML文件中用来分割文本的大量空格标签（理论上次操作不会影响HTML的内容显示，也做过简单的手动删除实验）
2， 将HTML文件转化为TXT数据，视为str整体进行关键字定位匹配
3， 通过关键字的位置数据，插入用来高亮显示的标签，即'<mark></mrk>'字符串
4， 将修改后的HTML字符串文件mark_html处理并保存为本地HTML文件夹'pdf2html/'下，重命名为'tr_'开头的新html文件
5， 前端调用本地'tr_'开头的新HTML文件，显示高亮关键字后的PDF文本
显示结果：
用户可以在新的网页上看到高亮后的文本内容，可以通过在页面，右击鼠标-->选择打印-->选择PDF格式，将高亮后的文件保存到本地
问题：
1， 只对html中每行内的空格分别进行去除空格标签处理，如果关键词是处在上下两行的尾首处，则无法被匹配高亮
2， 未用到有限状态机算法
3， 可以调用第三方库，将HTML生成PDF文件，此处考虑时间问题，暂未进一步实现，请在前端显示时提供将高亮后的文本保存为本地PDF文件的操作方法
4， pycharm的HTML源码显示问题，未得到最终的测试效果，请在各自的电脑按步骤操作
5， 碰到bug请及时提交到群里讨论
'''
# get_all_keywords用到的包
import jieba
from get_word2vec import get_word2vec
from pdfminer2txt import get_pdf2txt
import catchkeywords
import numpy as np
import re
import clean_html
import get_all_keywords

filename = 'test'
filepath = 'pdf/test.pdf'
stopwords_path = 'word2vec_format.txt'
html_file = 'pdf2html/test.html'
usr_keyword = ['计算机', '人工智能']
html_doc = clean_html.clean_html(html_file)


# 导入关键词列表，以备遍历
final_keywords = get_all_keywords.get_final_keywords(
    filepath, stopwords_path, usr_keyword)


def indexstr(str1, str2):
    # 查找指定字符串str1包含指定子字符串str2的全部位置，以列表形式返回
    lenth2 = len(str2)
    lenth1 = len(str1)
    indexstr2 = []
    i = 0
    while str2 in str1[i:]:
        indextmp = str1.index(str2, i, lenth1)
        indexstr2.append(indextmp)
        i = (indextmp + lenth2)
    return indexstr2


# 获取所有关键词在HTML文本字符串中的位置
loca_list = {}
for elem in final_keywords:
    elem_loca = indexstr(html_doc, elem)
    loca_list[elem] = elem_loca

# 根据关键词长度，逐个在关键词前后添加<mark></mark>标签
html_doc_lis = list(html_doc)
add_ltag = '<mark>'
add_rtag = '</mark>'
print(type(html_doc_lis))
for word, location in loca_list.items():
    len_word = len(word)
    len_location = len(loca_list[word])
    for i in range(len_location):
        html_doc_lis.insert(loca_list[word][i], add_ltag)
        html_doc_lis.insert(loca_list[word][i]+len_word+1, add_rtag)
mark_html = ''.join(html_doc_lis)

# 输出为HTML文件，保存到本地，后续由前端调用打开作为展示结果
output_name = 'tr_' + filename
output_path = 'pdf2html/' + output_name + '.html'
with open(output_path, "w", encoding='utf-8') as f:
    f.write(mark_html)
    f.close()
