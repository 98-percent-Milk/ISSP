from nltk.corpus import wordnet as wn
# Animal: cat, eagle
# Plant: dandelion, oak
# Food: banana, pizza
# Object: belt, comb, bottle
# Place: beach, kitchen
# Concept: pink, cone
# Person: musician, ankle


def main():
    test_words = ["cat", "eagle", "dandelion", "oak", "banana", "pizza", "belt",
                  "comb", "bottle", "beach", "kitchen", "pink", "cone", "musician", "ankle"]
    for word in test_words:
        test = FC(word)
        print(f"{word}: {test.wit}")


class FC:
    def __init__(self, word: str) -> None:
        self.word = word
        self.taste = ''
        self.color = ''
        self.texture = ''
        self.shape = ''
        self.wit = ''
        self.lex_names = self.__get_lex_names()
        self.__what_is_it()

    def __get_lex_names(self) -> list:
        return list(set(x.lexname() for x in wn.synsets(self.word)))

    def __is_it_place(self):
        for defi in [x.definition() for x in wn.synsets(self.word)]:
            print(defi)
            if 'area' in defi or 'place' in defi:
                return True
        return False

    def __what_is_it(self):
        if "noun.animal" in self.lex_names:
            self.wit = 'animal'
        elif "noun.person" in self.lex_names or "noun.body" in self.lex_names:
            self.wit = 'person'
        elif "noun.object" in self.lex_names:
            self.wit = 'object'
        elif "noun.food" in self.lex_names:
            self.wit = ["food", "fruit"][0 + ("noun.plant" in self.lex_names)]
        elif "noun.plant" in self.lex_names:
            self.wit = "plant"
        elif "noun.artifact" in self.lex_names or "noun.location" in self.lex_names:
            self.wit = "place"
        else:
            self.wit = "place" if self.__is_it_place() else "concept"


if __name__ == "__main__":
    main()
