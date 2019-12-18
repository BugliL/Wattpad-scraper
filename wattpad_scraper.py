#!/usr/bin/env python
# coding: utf8

from sys import argv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, Comment
import html
import flask


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


def get_story(soup):
    story = []
    title = str(soup.title.string).encode("ascii", 'ignore').decode("utf-8").partition("-")[0].strip()
    while soup:
        article_texts = soup.findAll(attrs={'data-p-id': True})
        chapter = u"\n".join(html.unescape(t.text).replace(u'\u2022' * 3, '').strip() for t in article_texts)
        story.append(chapter)

        next_page_url = get_next_page_url(soup)
        soup = parse_soup(next_page_url) if next_page_url else None

    return title, story


def get_next_page_url(soup):
    link = soup.find('a', class_="next-part-link", href=True)
    return link['href']


if __name__ == '__main__':
    url = argv[1]

    soup = parse_soup(url)
    title, story = get_story(soup)

    with open(f"{title}.txt", 'w', encoding='utf8') as FH:
        FH.writelines(story)
