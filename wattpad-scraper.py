#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, Comment
import html


# Copyright (c) 2018 Lorenzo Bugli
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def parse_soup(url):
    MOZILLA = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=MOZILLA)
    html_content = urlopen(req).read()
    return BeautifulSoup(html_content, 'html.parser')


if __name__ == '__main__':

    URL = argv[1]
    i = 1

    soup = parse_soup(URL)
    title = soup.title.string
    story = []
    while i == 1 or (str(i) in soup.title.string):
        print(soup.title.string)
        article_texts = soup.findAll(attrs={'data-p-id': True})
        chapter = u"\n".join(html.unescape(t.text).replace('•••', '').strip() for t in article_texts)
        story.append(chapter)

        i += 1
        page = URL + f'/page/{i}'
        soup = parse_soup(page)

    with open(f"{title}.txt", 'w') as FH:
        FH.writelines(story)
