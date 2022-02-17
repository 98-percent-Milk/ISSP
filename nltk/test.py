import json
from textwrap import indent
from nltk.corpus import wordnet as wn
from bs4 import BeautifulSoup as bs
from pprint import pprint
# Animal: cat, eagle
# Plant: dandelion, oak
# Food: banana, pizza
# Object: belt, comb, bottle
# Place: beach, kitchen
# Concept: pink, cone
# Person: musician, ankle


def main():
    # new_test('banana', 'fruit')
    # new_test('dog', 'fruit')
    # choose_topic('banana')
    # new_count_categories('person_category.json')
    words = ['cat', 'eagle', 'dandelion', 'oak', 'banana', 'pizza', 'belt', 'comb',
             'bottle', 'beach', 'kitchen', 'pink', 'cone', 'musician', 'ankle']
    for word in words:
        cat_test(word)


def cat_test(word):
    i = choose_topic(word)
    try:
        topic = wn.synsets(word)[i]
    except IndexError:
        print(wn.synsets(word), i)
        return
    hypo = topic.hyponyms()
    if hypo == []:
        hypo = topic.hypernyms()[0].hyponyms()
    #     category = list(set([x._lexname for x in hypo.hyponyms()]))
    # else:
    category = list(set([x._lexname for x in hypo]))
    print(f"{word:<10}:{category}")
    # for word in hypo[0].hyponyms():
    #     print(f"{word._lexname}: {word._lemma_names}")


def new_test(word: str, filename: str):
    save_json(word, filename)
    # collect_categories(filename)
    # new_count_categories(filename)


def new_count_categories(filename: str):
    with open(filename + '.json', 'r') as f:
        words = json.loads(f.read())
    print(f"Length: {len(words)}")
    count = {}
    for arr in words.values():
        for word in arr:
            try:
                count[word] += 1
            except KeyError:
                count[word] = 1
    count = {k: v for k, v in sorted(
        count.items(), key=lambda item: item[1], reverse=True)}
    for v, k in count.items():
        print(f"{v:<15}:{k}")
    category = max(count.items(), key=lambda x: x[1])
    in_and_out(words, category[0])


def in_and_out(words: dict, category: list):
    arr1 = []
    arr2 = []
    for v, k in words.items():
        if category in k:
            arr1.append(v)
        else:
            arr2.append(v)

    print(f"{'Inside':-^30}")
    print(arr1)
    print(f"\n{'Outside':-^30}")
    print(arr2)


def collect_categories(filename: str):
    data = []
    temp = {}
    with open(filename + '.json', 'r') as f:
        data = json.loads(f.read())

    with open(filename + '_category.json', 'w') as f:
        for person in data.keys():
            word_root(person, temp)
            categories = list(set([x.lexname() for x in wn.synsets(person)]))
            if categories != []:
                temp[person] = categories
            for word in data[person]:
                word_root(word, temp)
                categories = list(set([x.lexname()
                                  for x in wn.synsets(word)]))
                if categories != []:
                    temp[word] = categories
        f.write(json.dumps(temp, indent=4))


def save_json(word: str, filename: str):
    words = get_hyponyms(word)
    # with open(filename + '.json', 'w') as f:
    #     f.write(json.dumps(words, indent=4))


def nested_to_single(arr: list) -> list:
    if arr == []:
        return []
    subs = []
    list(map(lambda x: subs.extend(x), [x for x in arr])).remove(None)
    return subs


def choose_topic(word: str):
    syns = [x._lexname for x in wn.synsets(word)]
    def wc(a, b, c): return a.index(b) if a.index(
        b) < a.index(c) else a.index(c)
    i = 0
    if 'noun.animal' in syns and 'noun.person' in syns:
        i = wc(syns, 'noun.animal', 'noun.person')
    elif 'noun.plant' in syns and 'noun.food' in syns:
        i = syns.index('noun.food')
    return i


def get_hyponyms(word) -> dict:
    i = choose_topic(word)
    syns = [x._lemma_names for x in wn.synsets(word)[0].hypernyms()]
    syns = nested_to_single(syns)
    print(syns)
    # topic = wn.synsets(word)[0].hypernyms()[0]._lemma_names[0]
    # print(topic)
    topics = [x._lemma_names for x in wn.synsets(syns[0])[0].hyponyms()]
    print(topics)
    # subs = nested_to_single(topics)
    # temp = {}
    # for sub in subs:
    #     t = [x._lemma_names for x in wn.synsets(sub)[0].hyponyms()]
    #     temp[sub] = nested_to_single(t)
    # return temp


def count_categories(filename: str):
    with open(filename + '.json', 'r') as f:
        words = json.loads(f.read())
    count = {}
    try:
        for v in words.values():
            c = [x.split('.')[0] for x in v['categories']]
            for cat in c:
                try:
                    count[cat] += 1
                except KeyError:
                    count[cat] = 1
    except KeyError:
        pass
    count = {k: v for k, v in sorted(count.items(), key=lambda item: item[1])}
    for v, k in count.items():
        print(f"{v:<15}:{k}")


def get_animals(filename: str):
    # loading animal names
    with open(filename, 'r') as f:
        data = [x.strip() for x in f.readlines()]

    # declaring new empty animal dictionary
    animals = {}
    with open("animals.json", 'w') as fp:
        for animal in data:
            word_root(animal, animals)
        fp.write(json.dumps(animals, indent=4))


def word_root(word: str, topic: dict):
    topic[word] = {}
    # for x in wn.synsets(word):
    synsets = wn.synsets(word)
    try:
        synsets[0]
        # check if noun.animal/5 exist in the lexical categories
        cs = [x.lemmas()[0]._lexname_index for x in synsets]
        i = [x for x in list(range(len(cs))) if cs[x] == 5]
        for x in i:
            temp = []
            word_root_helper(synsets[x], temp)
            topic[word]['root'] = temp[-1]
            topic[word]['categories'] = temp
    except IndexError:
        print("Empty")
        topic.pop(word)


def word_root_helper(x, lisst):
    temp = x.hypernyms()
    if temp == []:
        lisst.append(x.name())
        return
    lisst.append(x.name())
    word_root_helper(temp[0], lisst)


def test(word: str):
    for x in wn.synsets(word):
        temp = list(x.tree(lambda s: s.hypernyms()))
        try:
            pprint(temp)
        except IndexError:
            pass


def find_common_category(filename: str) -> list:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    data = list(data.values())
    temp = set(data[0])
    for x in data[1:]:
        temp = set(x).intersection(temp)
        if len(temp) == 0:
            break
    print(temp)
    return temp


def extract_categories(filename: str) -> None:
    with open(filename, 'r') as f:
        data = [x.strip().lower() for x in f.readlines()]

    with open(filename.replace('txt', 'json'), 'w') as f:
        temp = {}
        for word in data:
            categories = list(set([x.lexname() for x in wn.synsets(word)]))
            if categories != []:
                temp[word] = categories
        f.write(json.dumps(temp, indent=4))


if __name__ == "__main__":
    main()
