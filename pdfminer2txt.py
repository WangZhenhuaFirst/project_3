# _*_ coding utf-8 _*_
'''
输入PDF文件（输入文件路径）
通过函数get_pdf2txt，调用pdfminer库，处理后返回TXT数据（数据类型为str）
输出TXT文本数据：str类型
'''


def get_pdf2txt(path):
    # 输入目标PDF路径，输出字符串形式的全文文本
    from pdfminer.pdfparser import PDFParser, PDFDocument
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.layout import LAParams, LTTextBox
    from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(open(path, 'rb'))
    # 创建一个PDF文档
    # doc = PDFDocument()
    doc = PDFDocument(praser)
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        output_txt = ''
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()

            for x in layout:
                if isinstance(x, LTTextBox):
                    output_txt += x.get_text()

    return output_txt


if __name__ == '__main__':
    output_txt = get_pdf2txt('pdf/test.pdf')
    with open('test.txt', 'w', encoding='utf-8') as f:
        f.write(output_txt)
