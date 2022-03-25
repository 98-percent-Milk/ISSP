import enum
import re
from requests import get
from bs4 import BeautifulSoup as bs
from pprint import pprint
from nltk.corpus import wordnet as wn
from datamuse import Datamuse
from json import dumps, loads
from association import get_association
API = Datamuse()
# cat = 2121620, and bird = 1613294
# python -W ignore (run without user warning)
# What does it look like word(_body_part)


def main():
    animals = [2121620, 1613294]
    # body_part = load_data('animal/body_part.json')
    habitat = load_data('animal/habitat.json')
    # test = words('cat_habitat')
    # word = off_to_syn(animals[0])
    check_location('cat')


def check_location(word: str, habitat: dict) -> None:
    raw = get_text(word)
    habitats = list(habitat.keys())
    for hab in habitats:
        print()


def get_text(word: str) -> str:
    raw = ''
    soup = get_soup(word)
    for tag in soup.find(id="Habitats").next_elements:
        if tag.name == 'p':
            raw += tag.text
        elif tag.name == 'h3':
            break
    return raw


def get_soup(word: str) -> bs:
    return bs(get(f"https://en.wikipedia.org/wiki/{word}").text, "html.parser")


def check_body_part(word: str, body_part: dict) -> None:
    syns = [x for x in wn.synsets(word) if x.name().split('.')[0] == word]
    for syn in syns:
        names = parents(syn, name=True)
        bnames = list(body_part.keys())
        if (temp := set(names).intersection(set(bnames))):
            print(f"{syn.name():<15}{temp}")
            break


def parents(syn: wn.synset, name: bool = False) -> list:
    synsets = list(syn.closure(lambda x: x.hypernyms()))
    return [x.name() for x in synsets] if name else synsets


def names(word: str) -> set:
    return set(x.name() for x in wn.synsets(word))


def off_to_syn(offset: int, pos: str = 'n') -> wn.synset:
    return wn.synset_from_pos_and_offset(pos, offset)


def words(word: str) -> list:
    return [x['word'] for x in API.words(ml=word)]


def load_data(filename: str = "files/category.json") -> dict:
    with open(filename, 'r') as f:
        data = loads(f.read())
    return data


if __name__ == "__main__":
    main()
