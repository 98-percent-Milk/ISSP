import enum
from pprint import pprint
from nltk.corpus import wordnet as wn
from json import dumps, loads
from association import get_association
# All the possible ways the word can be parsed through the search engine
# eagle, eagle.n.01, Syn(eagle.n.01), offset: 1613294
# we need word, category, and maybe synset


def main():
    data = load_data("files/new.json")
    forms = ['eagle', 'eagle.n.01', wn.synset('eagle.n.01'), 1613294]
    assn = association_words(forms[1], data)
    # trg = assn['trigger']
    for x in assn['trigger']:
        is_it_body_part(x)
    # new_test('wing')


def is_it_body_part(word: str, category: str = '') -> None:
    indexes = lexnames(word, category)
    syns = wn.synsets(word)
    for i in indexes:
        parent = get_parents(syns[i])
        if 'body_part.n.01' in parent:
            # can overgeneralized for person and animal
            print(f"{word} is animal body part")
            return


def is_it_habitat(word: str, category: str = '') -> None:
    # category = noun.object or noun location or noun.artifact
    indexes = lexnames(word, category)
    checks = [
        "structure.n.01",
        "biome.n.01",
        "land.n.04",
        "region.n.01",
        "habitat.n.01",
        "atmosphere.n.05"
        "geological_formation.n.01",
        "geographical_area.n.01",
        "vivarium.n.01"
    ]


def lexnames(word: str, category: str = '') -> None:
    temp = [x.lexname() for x in wn.synsets(word)]
    return [i for i, x in enumerate(temp) if x == category] if category else temp


def test(word: str) -> None:
    data = load_data("files/reverse.json")
    values = set([x for x in data['animal']])
    for syn in wn.synsets(word):
        parent = get_parents(syn)
        if (temp := list(parent.intersection(values))):
            print(f"{word} is {data['animal'][temp[0]]}")


def old(word: str, data: dict) -> list:
    n_syns = [[x.lexname().split('.')[1].replace('artifact', 'object'), x]
              for x in wn.synsets(word) if 'n' == x.pos()]
    non_n_syns = [[x.lexname(), x] for x in wn.synsets(word) if 'n' != x.pos()]
    for x in n_syns:
        try:
            main_cat = set(data[x[0]].keys())
            parents = get_parents(x[1])
            sub_cat = list(main_cat.intersection(parents))[0]
            print(f"{word:<30}{data[x[0]][sub_cat]}")
        except ValueError:
            pass


def association_words(word: str, data: dict = {}) -> None:
    if type(word) == int:
        # We know the exact synset of the word
        synset = offset_to_synset(word)
    else:
        # We don't know the exact synset of the word so all synset must be
        # searched
        # saddo something
        synset = wn.synset(word)
    infos = ecfs(synset, data)
    return get_association(infos[0], infos[2])


def ecfs(synset: wn.synset, data: dict):
    parents = get_parents(synset)
    top = synset.lexname().split('.')[1]
    sub_cat = set(data[top].keys())
    main_cat = list(parents.intersection(sub_cat))[0]
    if main_cat:
        # Word, synset_form, sub_category, main_category
        return [synset.name().split('.')[0], synset.name(), data[top][main_cat], top]


def get_parents(synset: wn.synset) -> set:
    return set([x.name()
                for x in list(synset.closure(lambda x: x.hypernyms()))])


def parents_from_synset(synset: wn.synset):
    return list(synset.closure(lambda x: x.hypernyms()))


def offset_to_synset(offset):
    """ offset -> synset form """
    return wn.synset_from_pos_and_offset('n', offset)


def load_data(filename: str = "files/category.json") -> dict:
    with open(filename, 'r') as f:
        data = loads(f.read())
    return data


if __name__ == '__main__':
    main()
