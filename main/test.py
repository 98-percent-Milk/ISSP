import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    word = ''
    while True:
        word = input("Enter word to search: ")
        if word == 'exit':
            break
        req = requests.get(url + word)
        for a in req.text:
            print(a)
        # soup = BeautifulSoup(req.text, 'html.parser')
        # print(soup.prettify())


if __name__ == '__main__':
    main()
