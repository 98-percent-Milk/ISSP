import re
from pprint import pprint
from textwrap import indent
from datamuse import Datamuse
from nltk.corpus import wordnet as wn
from os.path import join, realpath
from itertools import chain
from json import loads, dumps
API = Datamuse()


def main():
    data = load_data()
    # word = 'plant'
    # test = compound(word, data)
    # pprint(test)
    # head = test['head']
    # pprint(separate(head))
    # pprint(test)
    # word = 'banana'
    # a = before_adj(word)
    # pprint(a)
    # jb = set(jjb(word))
    # bb = set(bgb(word))
    # pprint(jb.intersection(bb))


def parents(word: str):
    for syn in wn.synsets(word):
        pprint(parent(syn))


def defis(word: str) -> wn.synset:
    syns = wn.synsets(word)
    for i in range(len(syns)):
        print(f"{i + 1}. {syns[i]._name:<15} {syns[i].definition()}")


def parent(word_syn: wn.synset) -> list:
    """ Returns all the parent categories that the word_syn belong to as a list """
    return list(word_syn.closure(lambda x: x.hypernyms()))


def child(word_syn: wn.synset) -> list:
    """ Returns all the words that belong to word_syn category as a list """
    return list(word_syn.closure(lambda x: x.hyponyms()))


def sib(word: str, tp: str = 'n', i: int = 1) -> wn.synset:
    """ Return the synset representation of the word. By default it will return 
        first noun synset """
    return wn.synset(f"{word}.{tp}.0{i}")


def load_data(filename: str = 'data.noun', dirname: str = 'wordnet') -> str:
    """ Returns all the nouns that are available in the wordnet data by default """
    with open(join(realpath(dirname), filename), 'r', encoding="utf-8") as f:
        data = f.read()
    return data


def compound_word(word: str, data: str, head: bool = True) -> list:
    """ From the wordlist match all the compound words that contains the word """
    return re.findall(r"{}_\w*\b".format(word), data) if head else re.findall(r"\w*_{}".format(word), data)


def compound(word: str, data: str) -> dict:
    """ Populate dictionary with compound words containing the parameter word """
    temp = {}
    temp['head'] = compound_word(word, data)
    temp['tail'] = compound_word(word, data, False)
    return temp


def not_noun(word: wn.synset):
    """ Extract derivationally related forms (noun) of adjs and verbs"""
    hypo = list(chain(*[x.lemmas()
                        for x in wn.synsets(word)]))
    hypo = list(chain(*[x.derivationally_related_forms() for x in hypo]))
    return [x._synset for x in hypo]


def separate(words: list):
    syns = [sib(x) for x in words]
    prnt = []
    chld = {}
    for i in range(len(syns)):
        syn = syns[i]
        temp = parent(syn)
        found = [x for x in temp if x in syns]
        if len(found) != 0:
            chld[syn._name] = found
        else:
            prnt.append(syn)
    temp = {
        "parent": set(prnt),
        "child": chld
    }
    return temp


def jja(word: str) -> list:
    """ Return list of Nouns that are often described by the adjective 'word' """
    return [x['word'] for x in API.words(rel_jja=word)]


def jjb(word: str) -> list:
    """ Return list of adjectives that are often used to describe the 'word' """
    return [x['word'] for x in API.words(rel_jjb=word)]


def trg(word: str) -> list:
    """ Return list of words that are triggered by (strongly associated with) the 'word' """
    return [x['word'] for x in API.words(rel_trg=word)]


def bga(word: str) -> list:
    """ Return list of words that are Frequent followers of 'word' """
    return [x['word'] for x in API.words(rel_bga=word)]


def bgb(word: str) -> list:
    """ Return list of words that are Frequent predecessors  of 'word' """
    return [x['word'] for x in API.words(rel_bgb=word)]


def before_adj(word: str) -> list:
    """Return list of adj that describes the word that are Frequent predecessors """
    adj = set(jjb(word))
    before = set(bgb(word))
    return adj.intersection(before)


if __name__ == "__main__":
    main()
