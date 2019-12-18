import tempfile

import flask
from wattpad_scraper import get_story, parse_soup
from flask import request, render_template, send_file

app = flask.Flask(__name__)


@app.route('/download-txt', methods=['POST'])
def download_txt():
    url = request.form['url']
    soup = parse_soup(url)
    title, story = get_story(url, soup)

    with tempfile.NamedTemporaryFile('w', encoding='utf8', delete=False) as temp:
        temp.writelines(story)
        temp.flush()

    return send_file(
        temp.name,
        as_attachment=True,
        mimetype='text/plain;charset=UTF-8',
        attachment_filename=title + ".txt"
    )


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8059, debug=True)
