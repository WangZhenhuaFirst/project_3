# _*_ coding utf-8 _*_
'''
观察PDF2htmlEX程序处理PDF文件生成的HTML代码发现其中很多无用标签，既不会影响内容输出，也不会影响网页结构
正则化去除其中的空格标签<span></span>
输出清理后的HTML文件
'''

import re


def clean_html(html_file1):
    with open(html_file1, encoding='utf-8') as f:
        html_content = f.read()
    clean_str_noblank = r'\<span.*?\>\s*'
    clean_str_end = r'\<\/span\>'
    after_clean2 = re.sub(clean_str_noblank, '', html_content)
    after_clean3 = re.sub(clean_str_end, '', after_clean2)
    return after_clean3


if __name__ == '__main__':
    html_file = 'data/html_file/test.html'
    after_clean = clean_html(html_file)
    print(after_clean)
