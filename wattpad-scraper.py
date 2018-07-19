from sys import argv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, Comment
import html


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
