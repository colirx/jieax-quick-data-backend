from flask import Flask, request, jsonify, render_template, abort
import os
from flask_cors import CORS

from utils import ParseSQLFile

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found!", 404


@app.route('/')
def index():
    return render_template('index.html', message='Hello from Flask!')


@app.route('/about')
def about():
    return 'This is the about page!'


@app.route('/user/<username>')
def show_user_profile(username):
    return f'User: {username}'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'You are logged in!'
    return 'Login page'


@app.route('/data')
def get_data():
    data = {"name": "Alice", "age": 25}
    return jsonify(data)


@app.route('/upload-page')
def upload_page():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    print(f'接收文件 {file.filename}……')
    if file.filename.endswith('.sql'):
        print('使用 SQL 工具解析处理……')
        ParseSQLFile.parse(file.filename)
    elif file.filename.endswith('.plantuml'):
        print('使用 plantuml 工具解析处理……')
    return jsonify({'message': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
