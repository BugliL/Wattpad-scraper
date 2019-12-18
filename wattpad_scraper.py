#!/usr/bin/env python
# coding: utf8
import re
import time
import urllib
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
    attempt = 0
    MOZILLA = {'User-Agent': 'Mozilla/5.0'}

    while True:
        try:
            req = Request(url, headers=MOZILLA)
            html_content = urlopen(req).read()
            return BeautifulSoup(html_content, 'html.parser')
        except urllib.error.HTTPError:
            if attempt > 3:
                raise

            attempt += 1


def get_story(url, soup):
    def strip_url(url):
        url = re.sub(r"/page/\d+", '', url)
        return url if url[-1] != '/' else url[:-1]

    def parse_title(soup):
        return str(soup.title.string).encode("ascii", 'ignore').decode("utf-8").partition("-")[0].strip()

    def parse_chapter_title(soup):
        return soup.find('article').find('h2').text.strip()

    def write_row(next_page_url):
        return "\n{}".format(str(next_page_url))

    def parse_text(soup):
        for br in soup.find_all("br"):
            br.replace_with("\n")

        return ['\n' + p.text.strip() for p in soup.findAll(attrs={'data-p-id': True})]

    def soup_or_none(page_url):
        return parse_soup(page_url) if page_url else None

    def create_page_string(i):
        return '/page/{}'.format(str(i))

    def parse_page_text(page_url):
        page = soup_or_none(page_url)
        page_text = parse_text(page)
        return page_text

    title = parse_title(soup)
    story = ['\n', title, '\n', ]
    next_chapter_url = strip_url(url)
    while soup and soup.find('article'):
        chapter_title = parse_chapter_title(soup)
        story.append(write_row(chapter_title))

        # Parse base page
        print(next_chapter_url)
        page = soup_or_none(next_chapter_url)
        page_text = parse_text(page)
        story += page_text

        # Parse next pages
        i = 2
        page_url = next_chapter_url + create_page_string(i)
        page_text = parse_page_text(page_url)
        while not all(row in story for row in page_text):
            print(page_url)
            story += page_text

            i += 1
            page_url = next_chapter_url + create_page_string(i)
            page_text = parse_page_text(page_url)

        next_chapter_url = get_next_page_url(soup)
        soup = soup_or_none(next_chapter_url)
        story.append(write_row(next_chapter_url))

    return title, story


def get_next_page_url(soup):
    link = soup.find('a', class_="next-part-link", href=True)
    return link['href'] if link else None


if __name__ == '__main__':
    url = argv[1]

    soup = parse_soup(url)
    title, story = get_story(soup)

    with open(f"{title}.txt", 'w', encoding='utf8') as FH:
        FH.writelines(story)
