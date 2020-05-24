# _*_ coding utf-8 _*_
'''
输入本地的wordembedding文件路径
读取wordembedding（txt格式，手动删除第一行统计信息，词与向量之间分别用空格分开）
输出Word2vec：字典类型，单词（key）-->向量（value）
'''


def get_word2vec(embed_file):
    # 读取word2vec文件，输出word2vec的词-向量字典
    word2vec = {}
    input = open(embed_file, 'r', encoding='utf-8')

    lines = []
    for line in input:
        lines.append(line)
    nwords = len(lines)
    splits = lines[0].split(' ')
    dim = len(splits) - 1

    embeddings = []
    for lineId in range(len(lines)):
        splits = lines[lineId].split(' ')
        if len(splits) > 2:
            # embeddings赋值
            emb = [float(splits[i]) for i in range(1, len(splits))]
            embeddings.append(emb)
            # word2vec赋值
            word2vec[splits[0]] = embeddings[lineId]

    return word2vec


if __name__ == '__main__':
    word2vec = get_word2vec('word2vec_format.txt')
    print(type(word2vec['，'][0]))




