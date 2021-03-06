from operator import truediv
from datamuse import Datamuse
from json import loads, dumps
from pprint import pprint
from nltk.corpus import wordnet as wn
from itertools import chain


def main():
    word = input("Enter word: ")
    score = int(input("Enter score limit: "))
    filename = 'food.json'
    with open(filename, 'r', encoding="utf-8") as f:
        data = loads(f.read())

    # word = 'banana'
    api = Datamuse()
    before = [x['word']
              for x in api.words(rel_bgb=word) if x['score'] >= score]
    for be in before:
        if is_color(be):
            print(f"{be:<10} is color")
        elif is_size(be):
            print(f"{be:<10} is size")
        for key in data.keys():
            if be in data[key]:
                print(f"{be:<10} is {key}")

    after = [x['word'] for x in api.words(rel_bga=word) if x['score'] >= score]
    for af in after:
        if think_of(af):
            print(f"{word:<10} makes me think {af:^15}or goes with {af:^15}")


def think_of(word):
    hypo = [x._lexname for x in wn.synsets(word, wn.NOUN)]
    return True if ('noun.food' in hypo or 'noun.plant' in hypo) else False


def is_color(word):
    color = wn.synset('color.n.01')
    hypo = [x.lowest_common_hypernyms(color) for x in wn.synsets(word)]
    return True if color._name in [x[0]._name for x in hypo if x != []] else False


def is_taste(word):
    taste = wn.synset('taste_property.n.01')
    props = list(
        chain(*[x._lemma_names for x in list(taste.closure(lambda x: x.hyponyms()))]))
    return True if word in props else False


def is_shape(word):
    shape = wn.synset('shape.n.02')
    hypo = [x.lowest_common_hypernyms(shape) for x in wn.synsets(word)]
    return True if shape._name in [x[0]._name for x in hypo if x != []] else False


def is_size(word):
    size = wn.synset('size.n.01')
    hypo = wn.synsets(word, wn.NOUN)
    if hypo == []:
        hypo = not_noun(word)
    result = [ancestor(x, size) for x in hypo]
    return True if size in result else False


def not_noun(word):
    hypo = list(chain(*[x.lemmas()
                        for x in wn.synsets(word)]))
    hypo = list(chain(*[x.derivationally_related_forms() for x in hypo]))
    # for hyp in hypo:
    #     temp.extend(hyp)
    return [x._synset for x in hypo]


def ancestor(a, b):
    temp = a.lowest_common_hypernyms(b)
    return temp[0] if temp != [] else wn.synset('entity.n.01')


if __name__ == "__main__":
    main()
