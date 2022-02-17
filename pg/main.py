from nltk.corpus import wordnet as wn
from itertools import chain
from pprint import pprint


def main():
    words = ['red', 'cactus', 'dandilion', 'box', 'cross', 'pink',
             'green', 'big', 'olive', 'eagle', 'small', 'person']
    # for word in words:
    #     print(f"{word:<10} is {['not a color', 'color'][is_color(word)]}")
    # is_texture('big')
    # pprint(not_noun('big'))
    # pprint(not_noun('putrid'))
    not_noun('putrid')
    # print(f"{word} is {['not size', 'size'][is_size(word)]}")

# .derivationally_related_forms()


def not_noun(word):
    hypo = [x.lemmas()[0].derivationally_related_forms()
            for x in wn.synsets(word)]
    temp = []
    hypo = [temp.extend(x) for x in hypo if x != []]
    # for hyp in hypo:
    #     temp.extend(hyp)
    return [x._synset for x in temp]


def flatten(arr):
    temp = []
    help_flatten(arr, temp)
    return temp


def help_flatten(arr, temp):
    if len(arr) == 1:
        temp.append(arr)
        return
    temp.extend(arr.pop())
    help_flatten(arr, temp)


def is_size(word):
    size = wn.synset('size.n.02')
    hypo = wn.synsets(word, wn.NOUN)
    if hypo == []:
        hypo = not_noun(word)
    result = [ancestor(x, size) for x in hypo]
    return True if size in result else False
    # for hyp in hypo:
    #     print(
    #         f"Lowest:\n\t{ancestor(hyp, size)}\nSim:\n\t{hyp.wup_similarity(size)}")


def is_texture(word):
    texture = wn.synset('texture.n.04')
    hypo = wn.synsets(word, wn.NOUN)
    if hypo == []:
        hypo = not_noun(word)
    # pprint(hypo)
    for hyp in hypo:
        print(
            f"Lowest:\n\t{ancestor(hyp, texture)}\nSim:\n\t{hyp.wup_similarity(texture)}")


def ancestor(a, b):
    return a.lowest_common_hypernyms(b)[0]


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


if __name__ == "__main__":
    main()
