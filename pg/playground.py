from textwrap import indent
from unicodedata import category
from nltk.corpus import wordnet as wn
from json import loads, dumps
from os.path import join, realpath
from pprint import pprint

# Animal: cat, eagle
# Plant: dandelion, oak
# Food: banana, pizza
# Object: belt, comb, bottle
# Place: beach, kitchen
# Concept: pink, cone
# Person: musician, ankle


def main():
    words = ['cat', 'eagle', 'dandelion', 'oak', 'banana', 'pizza', 'belt',
             'comb', 'bottle', 'beach', 'kitchen', 'pink', 'cone', 'musician', 'ankle']
    word = 'cat'
    # fil = ['person.n.01', 'animal.n.01']
    # is_it_location('kitchen')
    # test('belt')
    for word in words:
        # test(word)
        if is_it_alive(word) == 'object':
            # test(word)
            pass
        else:
            print(f"Alive {word}")


def sibling(word) -> list:
    return wn.synsets(word)


def parent(syns) -> list:
    return list(syns.closure(lambda x: x.hypernyms()))


def child(syns) -> list:
    return list(syns.closure(lambda y: y.hyponyms()))


def test(word):
    bish = ['noun.food', 'noun.person', 'noun.plant', 'noun.animal']
    temp = [x for x in wn.synsets(
        word) if x._lemma_names[0] == word if x._lexname not in bish]
    for t in temp:
        tree = [x._name
                for x in list(t.closure(lambda x: x.hypernyms()))]
        print(f"{t._lexname:<20}\t{tree}", end='\n\n')


def is_it_location(word):
    category = ['location.n.01', 'room.n.01', 'area.n.05',
                'structure.n.01', 'geological_formation.n.01']
    cat = 'object'
    temp = [x for x in wn.synsets(word) if x._lemma_names[0] == word]
    for t in temp:
        tree = [x._name
                for x in list(t.closure(lambda x: x.hypernyms()))]
        for c in category:
            if c in tree:
                print(t, tree)
                cat = c.split('.')[0]
                break
    print(f"{word:<20}{cat}")


def is_it_alive_helper(arr):
    cat = ''
    if 'noun.plant' in arr[2]:
        cat = 'fruit' if 'noun.food' in arr[2] else 'plant'
    else:
        cat = 'animal' if 'noun.animal' in arr[2] else 'person'
    return cat


def is_it_alive(word):
    family = wn.synset('organism.n.01')
    temp, temp_l = [], []
    for syns in [x for x in wn.synsets(word) if x._lemma_names[0] == word]:
        t = family.lowest_common_hypernyms(syns)
        if t != []:
            temp.append(t[0]._name)
            temp_l.append(syns._lexname)
    if family._name in temp:
        if 'noun.artifact' in temp_l or 'noun.attribute' in temp_l:
            cat = False  # 'not_organism'
        else:
            cat = True  # 'organism'
    else:
        cat = False  # 'not_organism'
    if cat:
        category = is_it_alive_helper([cat, temp, temp_l])
    else:
        category = 'object'
    return category


def flatten(arr):
    temp = []
    help_flatten(arr, temp)
    return temp


def help_flatten(arr, temp):
    if len(arr) == 1:
        return
    temp.append(arr[0])
    help_flatten(arr[1], temp)


def royal_family(filename: str, term: str) -> None:
    with open(filename + '.json', 'r', encoding='utf-8') as f:
        words = loads(f.read())
        words = words[filename]
    temp = {}
    for word in words:
        for w in wn.synsets(word):
            t = [x._lemma_names[0]
                 for x in w.hypernyms() if term == x._lexname]
            try:
                temp[word].extend(t)
            except KeyError:
                temp[word] = []
                temp[word].extend(t)
            except IndexError:
                pass

    save_dict(temp, filename + '_category.json')


def blood_family(filename: str) -> None:
    with open(filename + '.json', 'r', encoding='utf-8') as f:
        words = loads(f.read())
        words = words[filename]
    temp = {}
    for word in words:
        for w in wn.synsets(word):
            t = [x._lemma_names
                 for x in w.hypernyms()]  # fix the iterable unpacking problem nested loop
            try:
                temp[word].extend(t)
            except KeyError:
                temp[word] = []
                temp[word].extend(t)
            except IndexError:
                pass
    print(temp['elderberry'])
    # save_dict(temp, filename + '_category.json')


def collect_decendants(word: str, temp: dict = {}, hypo: list = []) -> str:
    """
        Collect all the words that belongs to same lexical group
        Steps
        1. Get all definitions of the word wn.synsets(word)
        2. Filter definitions based on first lemma term word == x._lemma_names[0]
        3. Collect all words belong to specific lexical group
        4. Save words to .json file
    """
    name = hypo[0]._lemma_names[0]
    temp[name] = []
    for w in hypo:
        for sw in w.hyponyms():
            temp[name].extend(wn.synset(sw._name)._lemma_names)
    save_dict(temp, name + '.json')
    return name


def parent_description(word: str = '', hypo: list = []):
    """
    Steps
    1. Get all definitions of the word wn.synsets(word)
    2. Filter definitions based on first lemma term word == x._lemma_names[0]
    3. Populate temporary dictionary by its category
    object = Current -> noun.artifact | Parent Category -> tool, device, accessory
    """
    temp = {}
    for w in hypo:
        try:
            temp[w._lexname].extend(
                w.hypernyms()[0]._lemma_names)
        except KeyError:
            temp[w._lexname] = []
            temp[w._lexname].extend(w.hypernyms()[0]._lemma_names)
    return temp


def count_decendants(filename: str):
    """
    Count the most common category in the given words
    """
    with open(filename, 'r', encoding="utf") as f:
        words = loads(f.read())
    c = {}
    for terms in words.values():
        for term in terms:
            try:
                c[term] += 1
            except KeyError:
                c[term] = 1
    c = {k: v for k, v in sorted(c.items(), key=lambda item: item[1])}
    top = max(c.items(), key=lambda item: item[1])
    print(f"Total: {len(words.keys())}: Top: {top}")


def save_dict(terms: dict, filename: str = 'test.json', mode: str = 'w') -> None:
    data = terms
    with open(join(realpath('out'), filename), 'r', encoding='utf-8') as f:
        data = loads(f.read())

    with open(join(realpath('out'), filename), mode, encoding='utf-8') as f:
        f.write(dumps(data, indent=4))


if __name__ == "__main__":
    main()
