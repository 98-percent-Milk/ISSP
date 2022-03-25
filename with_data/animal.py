import enum
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
    location = load_data('animal/location.json')
    word = off_to_syn(animals[0])
    test = words('cat_habitat')
    for t in test:
        check_location(t, location)


def check_location(word: str, location: dict) -> None:
    syns = [x for x in wn.synsets(word)]
    for syn in syns:
        names = parents(syn, name=True)
        bnames = list(location.keys())
        if (temp := set(names).intersection(set(bnames))):
            print(f"{syn.name():<25}{temp}")
            break


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
