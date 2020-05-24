# _*_ coding utf-8 _*_
'''
调取catchkeywords得到的关键字列表，作为第一部分要输出的关键字
根据用户输入的主题词匹配TXT中的类似词语，作为第二部分要输出的关键字
将两部分合并，得到所有要展示给用户的关键字列表
后续对HTML文件中的这些关键字进行高亮标注
'''

import jieba
from get_word2vec import get_word2vec
from pdfminer2txt import get_pdf2txt
import catchkeywords
import numpy as np


def stopwordslist():
    # 根据目录保存的停用词TXT文件，生成停用词list备用
    stopwords = [line.strip() for line in open(
        'stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords


def seg_depart(txt_str):
    # 通过主函数调取处理PDF得到的txt内容，输出切分去重后的全文的词语list-->get_words
    sentence_depart = jieba.cut(txt_str.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    get_words = list(set(list(outstr.split())))
    return get_words


def get_dist(v1, v2):
    # 计算句向量余弦距离的函数
    words_dist = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return words_dist


def get_final_keywords(file_path, embed_file, usr_keyword):
    # 输入目标PDF文件路径，tfidf算法得到的关键词，用户输入的关键词usr_keyword（list类型）输出全文关键词
    input_txt = get_pdf2txt(file_path)
    get_words = seg_depart(input_txt)
    embedding_words = get_word2vec(embed_file)
    tfidf_keywords = catchkeywords.tfidf_extract(input_txt)

    usr_keywords = []
    for key_word in usr_keyword:
        # 对于用tfidf算法得到的每个关键词进行全文词距离计算，得到每个词的近义词作为相关关键词，输出到相关关键词列表
        distance = {}
        for text_word in get_words:
            if key_word in embedding_words and text_word in list(embedding_words.keys()) and text_word not in tfidf_keywords:
                distance[text_word] = get_dist(
                    embedding_words[key_word], embedding_words[text_word])

        res = sorted(distance.items(), key=lambda d: d[1], reverse=True)
        if res:
            usr_keywords.append(res[0][0])

    final_keywords = tfidf_keywords + usr_keywords
    return final_keywords


if __name__ == '__main__':
    file_path = 'test.pdf'
    embedfile_path = 'word2vec_format.txt'
    usr_keyword = ['计算机', '人工智能']
    print(get_final_keywords(file_path, embedfile_path, usr_keyword))
