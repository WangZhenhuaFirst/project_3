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
4， 将修改后的HTML字符串文件mark_html处理并保存为本地HTML文件夹'data/html_file/'下
5， 前端调用本地新HTML文件，显示高亮关键字后的PDF文本
'''


import clean_html
import get_all_keywords
from pdf_to_html import pdf_to_html


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


def get_result(file_path, file_name, subject_words):
    pdf_to_html(file_name)
    bare_filename = file_name.split('.')[0]
    html_file_path = 'data/html_file/' + bare_filename + '.html'
    html_doc = clean_html.clean_html(html_file_path)

    # 导入关键词列表，以备遍历
    final_keywords = get_all_keywords.get_final_keywords(
        file_path, subject_words)

    # 获取所有关键词在HTML文本字符串中的位置
    loca_dic = {}
    for elem in final_keywords:
        elem_loca = indexstr(html_doc, elem)
        loca_dic[elem] = elem_loca
    # 构造辅助列表
    prepare_list = []
    for k, v in loca_dic.items():
        prepare_list.append((k, v))
    # 获取字典{位置:关键字}
    loca_word = {}
    for i in range(len(prepare_list)):
        for n in prepare_list[i][1]:
            loca_word[n] = prepare_list[i][0]

    # 按键值大小排序,键为位置数据（int型），value为关键字， 但是字典是没有顺序的，所以转换为列表，列表元素为列表对
    loca_word_tuple = sorted(
        loca_word.items(), key=lambda dict: dict[0], reverse=False)  # 此为列表内的元组对
    loca_word_list = []
    for ele in loca_word_tuple:
        loca_word_list.append(list(ele))

    # 根据关键词位置，逐个在关键词前后添加<mark></mark>标签
    html_doc_lis = list(html_doc)
    add_ltag = '<mark>'
    add_rtag = '</mark>'

    for i in range(len(loca_word_list)):
        html_doc_lis.insert(loca_word_list[i][0], add_ltag)
        for ele in loca_word_list:
            ele[0] += 1
        html_doc_lis.insert(
            loca_word_list[i][0] + len(loca_word_list[i][1]), add_rtag)
        for ele in loca_word_list[(i+1):]:
            ele[0] += 1
    mark_html = ''.join(html_doc_lis)

    # 输出为HTML文件，保存到本地，后续由前端调用打开作为展示结果
    output_path = 'server/static/' + bare_filename + '.html'
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(mark_html)
        f.close()

    return final_keywords
