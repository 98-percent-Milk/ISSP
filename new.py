# import re
from pprint import pprint
# import nltk
# from datamuse import Datamuse
from nltk.corpus import wordnet as wn
from json import dumps, loads


def main():
    nltk.download("wordnet")
    # data = load_data("files/new.json")
    # r = True
    # while r:
    #     test(data, r := input("Enter word: "))
    #     if r == 'exit':
    #         break

    # # pprint(data)
    # # word = input("Enter word: ")
    # words = ['beans', 'bacon', 'bruschetta', 'bok_choy', 'bouquet', 'blanket']
    # for word in words:
    #     new_check(word, data)


def test(category, word=''):
    temp = {"first": [], "second": [], 'not_found': True}
    if word == '':
        with open('test.json', 'r') as f:
            data = loads(f.read())

        for word in data:
            syn = wn.synset_from_pos_and_offset(wn.NOUN, int(data[word]))
            offset_check(syn, category, word)
    syns = wn.synsets(word)
    for syn in syns:
        offset_check(syn, category, temp, word)
    if not temp['not_found']:
        print(f"{'Main Category':-^70}")
        display(temp['first'][0])
        print(f"{'Secondary Possible Category':-^70}")
        for arr in temp['second']:
            display(arr)


def display(arr: list) -> None:
    word = arr[0]
    syn = arr[1]
    category = arr[2]
    print(f"{word:<30}{syn:<30}{category:<30}")


def offset_check(syn: wn.synset, category: list, temp, word: str = ''):
    parent = [x._name for x in list(syn.closure(lambda x: x.hypernyms()))]
    for key in category:
        syns = category[key]
        for s in parent:
            if s in syns:
                if temp['not_found']:
                    # print(f"Main: {str(word).split('.')[0]:<30}{str(s):<30} {syns[s]}".format(
                    #     temp["first"]))
                    temp['first'].append([str(word), str(s), str(syns[s])])
                    temp['not_found'] = False
                # print(f"Secondary: {str(word).split('.')[0]:<30}{str(s):<30} {syns[s]}".format(
                #     temp["first"]))
                temp['second'].append([str(word), str(s), str(syns[s])])


def check(word: str, data: dict) -> None:
    syns = wn.synsets(word, wn.NOUN)
    for syn in syns:
        parents = set(x._name for x in list(
            syn.closure(lambda x: x.hypernyms())))
        for k in data.keys():
            group = set(data[k].keys())
            if parents.intersection(group):
                print(word)
                print(f"General category is : {k}")
                print(f"Possible Sub categories is/are : {group}")
                return


def new_check(word: str, data: dict) -> None:
    syns = wn.synsets(word, wn.NOUN)
    for syn in syns:
        parents = list(x._name for x in list(
            syn.closure(lambda x: x.hypernyms())))
        for k in data.keys():
            subk = data[k].keys()
            for sk in parents:
                if sk in subk:
                    print(
                        f"\nWord: {word}\nSpecific category is {sk}\nGeneral category is {k}\n")
                    return


def load_data(filename: str = "files/category.json") -> dict:
    with open(filename, 'r') as f:
        data = loads(f.read())
    return data


if __name__ == '__main__':
    main()
