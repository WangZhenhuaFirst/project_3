from flask_cors import CORS
from flask import Flask, jsonify, request

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
    file_name = file.filename
    # print(f"file: {file}")
    print(f"file_name: {file_name}")

    subject_words = request.form["subject_words"].split(',')
    # print(subject_words)
    # if subject_words:

    keywords = ['关键词一', '关键词二', '关键词三', '关键词四']

    path = f'./server/static/{file_name}'
    file.save(path)

    return jsonify({
        'download_url': f'http://localhost:5000/static/{file_name}',
        'keywords': keywords
    })


if __name__ == '__main__':
    app.run()
