import flask
from flask import request, render_template

app = flask.Flask(__name__)


@app.route('/download-txt')
def download_txt():
    url = request.form['url']



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8059, debug=True)
