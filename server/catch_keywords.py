# _*_ coding utf-8 _*_
'''
输入PDF文件，转换为txt文件
通过jieba库分别调用texttrank算法和tfidf算法，提取txt文件的关键字
输出指定个数的txt文件的关键词：存为list类型
通过对几个中文文档的关键字提取效果测试，后续采用tfidf算法提取关键字
'''

from jieba import analyse


def textrank_extract(text, keyword_num=5):
    # 输入PDF文本字符串，根据textrank算法输出关键词
    textrank = analyse.textrank
    analyse.set_stop_words('data/stopwords.txt')
    keywords = textrank(text, keyword_num)
    return keywords


def tfidf_extract(text, keyword_num=5):
    # 输入PDF文本字符串，根据tfidf算法输出关键词
    tfidf = analyse.extract_tags
    analyse.set_stop_words('data/stopwords.txt')
    keywords = tfidf(text, keyword_num)
    return keywords


if __name__ == '__main__':
    with open(file='test.txt', mode='r', encoding='utf-8') as f:
        text = f.read()
    print('TF-IDF模型结果：')
    tfidf_extract(text)
    print('TextRank模型结果：')
    textrank_extract(text)
