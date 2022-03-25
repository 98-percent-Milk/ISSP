from pprint import pprint
from nltk.corpus import wordnet as wn
from json import dumps, loads
from association import get_association
WORDS = ["cat.n.01", "eagle.n.01", "dandelion.n.01", "palm.n.03", "banana.n.02",
         "pizza.n.01", "bottle.n.01", "belt.n.02", "comb.n.01", "beach.n.01"]


def main():
    data = load_data("files/new.json")
    # pprint(data)
    # extract_data("eagle.n.01", data)
    word = 'eagle'
    category = 'bird'
    temp = get_association(word, category)
    trg = temp['after']
    for word in trg:
        test(data, word)


def extract_data(word: str, data: dict) -> None:
    temp = search_by_word(word, data)
    attn = get_association(temp[0], temp[2])
    for word in attn['trigger']:
        print(search_by_word)


def search_by_word(word: str, data: dict) -> list:
    syn = wn.synset(word)
    parent = set([x.name()
                 for x in list(syn.closure(lambda x: x.hypernyms()))])
    for category in data:
        sub_cat = set(data[category])
        if (temp := list(sub_cat.intersection(parent))):
            return [word.split('.')[0], temp[0],
                    data[category][temp[0]], category]


def test(category, word=''):
    temp = {"first": [], "second": [], 'not_found': True}
    try:
        """Categorizing word from unique 8 digit value"""
        word = int(word)
        syn = wn.synset_from_pos_and_offset(wn.NOUN, word)
        offset_check(syn, category, temp, syn._name.split('.')[0])
        display(temp)
    except ValueError:
        """ Categorizing word from the word form """
        word.replace(' ', '_')
        syns = wn.synsets(word)
        for syn in syns:
            offset_check(syn, category, temp, word)
        display(temp)


def display(temp: dict) -> None:
    if not temp['not_found']:
        print(f"{'Main Category':-^110}")
        print(f"{'Word':<30}{'Synset':<30}{'Sub Category':<30}{'Main Category':<30}")
        display_helper(temp['first'][0])
        # print(f"{'Secondary Possible Category':-^110}")
        # print(f"{'Word':<30}{'Synset':<30}{'Sub Category':<30}{'Main Category':<30}")
        # for arr in temp['second']:
        #     display_helper(arr)


def display_helper(arr: list) -> None:
    word = arr[0]
    syn = arr[1]
    sub_category = arr[2]
    main_category = arr[3]
    print(f"{word:<30}{syn:<30}{sub_category:<30}{main_category:<30}")


def offset_check(syn: wn.synset, category: list, temp, word: str = ''):
    parent = [x._name for x in list(syn.closure(lambda x: x.hypernyms()))]
    for key in category:
        syns = category[key]
        for s in parent:
            if s in syns:
                if temp['not_found']:
                    temp['first'].append(
                        [str(word), str(s), str(syns[s]), str(key)])
                    temp['not_found'] = False
                temp['second'].append(
                    [str(word), str(s), str(syns[s]), str(key)])


def load_data(filename: str = "files/category.json") -> dict:
    with open(filename, 'r') as f:
        data = loads(f.read())
    return data


if __name__ == '__main__':
    main()
