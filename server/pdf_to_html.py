import os


def pdf_to_html(file_name):
    os.system(
        f'pdf2htmlEX --zoom 1.3 data/pdf_file/{file_name} --dest-dir data/html_file')
