from textwrap import indent
import requests
from bs4 import BeautifulSoup as bs
import json


def main():
    texture = {'texture': []}
    with open('texture.html', 'r', encoding='utf-8') as f:
        soup = bs(f, 'html.parser')
    tds = soup.findAll('td')
    # tds = [x.text for x in tds]
    # print(len(tds))
    for td in tds:
        if (word := td.text) != '\xa0':
            texture['texture'].append(word)

    with open('textures.json', 'w') as f:
        f.write(json.dumps(texture, indent=4))


if __name__ == '__main__':
    main()
