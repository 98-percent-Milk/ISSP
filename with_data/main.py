from nltk.corpus import wordnet as wn
from json import dumps, loads
from pprint import pprint


def main():
    is_object('comb')
    is_location('beach')
    is_location('kitchen')


def is_object(word):
    cate = wn.synset('artifact.n.01')  # a man-made object taken as a whole
    hypo = []
    for syn in wn.synsets(word):
        if cate in (temp := list(syn.closure(lambda x: x.hypernyms()))):
            hypo.append([syn, temp])
    pprint(hypo)


def is_location(word):
    cate = [
        wn.synset("structure.n.01"),
        wn.synset("geological_formation.n.01")
    ]
    hypo = []
    for syn in wn.synsets(word):
        if cate[0] in (temp := list(syn.closure(lambda x: x.hypernyms()))):
            hypo.append([syn, temp])
        elif cate[1] in (temp := list(syn.closure(lambda x: x.hypernyms()))):
            hypo.append([syn, temp])
    pprint(hypo)


if __name__ == "__main__":
    main()
