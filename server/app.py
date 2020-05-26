from flask_cors import CORS
from flask import Flask, jsonify, request
import highlight_html

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


# sanity check route
@app.route('/', methods=['POST'])
def commit():
    file = request.files["file"]
    file_name = file.filename.replace(' ', '')
    file_path = f'./data/pdf_file/{file_name}'
    file.save(file_path)
    # print(f"file: {file}")
    print(f"file_name: {file_name}")

    subject_words = request.form["subject_words"].split(',')
    # print(subject_words)

    html_file_name = file_name.split('.')[0] + '.html'
    keywords = highlight_html.get_result(file_path, file_name, subject_words)

    # server_path = "http://127.0.0.1:5000"
    server_path = "http://l3132c3923.qicp.vip/"
    return jsonify({
        'download_url': f'{server_path}/static/{html_file_name}',
        'keywords': keywords
    })


if __name__ == '__main__':
    app.run()
