import re
from pprint import pprint
from datamuse import Datamuse
from nltk.corpus import wordnet as wn
from json import dumps, loads


def main():
    data = load_data("files/new.json")
    r = True
    while r:
        test(data, r := input("Enter word: "))
        if r == 'exit':
            break


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
