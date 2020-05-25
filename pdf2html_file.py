# _*_ coding utf-8 _*_
'''
输入原始PDF文件路径
调用PDF2htmlEX程序，将PDF转换为HTMl文件
输出html文件，并保存到'pdf2html/'文件夹下，与原始PDF文件同名
'''

import subprocess
import os


def get_html_file(filename1):
    # 输入目标PDF文件名，输出生成到本地的html文件路径
    local_path = os.getcwd().replace('\\','/')
    filename2 = filename1
    comment_set = local_path + r'/pdf2htmlEX_path/pdf2htmlEX.exe' + r' --zoom 1.3 pdf/' + filename2 + r'.pdf ' + r'--dest-dir pdf2html'
    subprocess.run(comment_set, shell=True)
    html_file = local_path + '/pdf2html/' + filename2 + '.html'
    return html_file


if __name__ == '__main__':
    filename = 'test'
    get_html_file('test')
