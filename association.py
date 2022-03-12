from unicodedata import category
from datamuse import Datamuse
from pprint import pprint
from nltk.stem import WordNetLemmatizer
API = Datamuse()
WNL = WordNetLemmatizer()


def main():
    word = 'cow'
    category = 'animal'
    test(word, category)
    noun(word, category=category)
    verb(word, category=category)
    adj(word, category=category)
    adv(word, category=category)


def test(word: str, category: str = '', pos: str = '') -> None:
    temp = association_dict(word=word, category=category, pos=pos)
    word_after = set([WNL.lemmatize(x) for x in temp['after']])
    word_before = set([WNL.lemmatize(x) for x in temp['before']])
    word_trigger = set([WNL.lemmatize(x) for x in temp['trigger']])
    print(word_after)
    print(word_before)
    print(word_trigger)


def everything(word: str, category: str = '') -> None:
    noun(word, category=category)
    verb(word, category=category)
    adj(word, category=category)
    # will return empty list if the word in question is not verb
    adv(word, category=category)


def noun(word: str, category: str = '') -> None:
    """ Display all the noun words that are associated with the 'word' """
    print(f"\n{'Noun':-^120}")
    association_display(word, category=category, pos='n')
    print(f"{'Noun':-^120}\n")


def verb(word: str, category: str = '') -> None:
    """ Display all the verb words that are associated with the 'word' """
    print(f"\n{'Verb':-^120}")
    association_display(word, category=category, pos='v')
    print(f"{'Verb':-^120}\n")


def adj(word: str, category: str = '') -> None:
    """ Display all the adjective words that are associated with the 'word' """
    print(f"\n{'Adjective':-^120}")
    association_display(word, category=category, pos='adj')
    print(f"{'Adjective':-^120}\n")


def adv(word: str, category: str = '') -> None:
    """ Display all the adverb words that are associated with the 'word' """
    print(f"\n{'Adverb':-^120}")
    association_display(word, category=category, pos='adv')
    print(f"{'Adverb':-^120}\n")


def association_dict(word: str, category: str = '', pos: str = '') -> dict:
    """
        Return dict of words that frequent predecessors, followers and strongly 
        associated words of the 'word'
    """
    temp = {
        "before": before(word=word, category=category, pos=pos),
        "after": after(word=word, category=category, pos=pos),
        "trigger": trigger(word=word, category=category, pos=pos)
    }
    return temp


def association_display(word: str, category: str = '', pos: str = '') -> None:
    """
        Display words that frequent predecessors, followers and strongly associated
        words of the 'word'
    """
    print('Before')
    print(before(word, category, pos))
    print('After')
    print(after(word, category, pos))
    print('Trigger')
    print(trigger(word, category, pos))


def before(word: str, category: str = '', pos: str = '') -> list:
    """
        Returns list of words that are FREQUENT PREDECESSORS of the 'word'
        Can be filtered further down by passing extra attributes such as category and part of speech
        category: (animal, plant, and etc)
        pos: noun -> n, verb -> v, adj -> adj, adverb -> adv
        by default category and pos are null
    """
    words = [x if pos else x['word']
             for x in API.words(rel_bgb=word, ml=word, topics=category, md='p') if 'tags' in x]

    return [x['word'] for x in words if pos in x['tags']] if pos else words


def after(word: str, category: str = '', pos: str = '') -> list:
    """
        Returns list of words that are FREQUENT FOLLOWERS of the 'word'
        Can be filtered further down by passing extra attributes such as category and part of speech
        category: (animal, plant, and etc)
        pos: noun -> n, verb -> v, adj -> adj, adverb -> adv
        by default category and pos are null
    """
    words = [x if pos else x['word']
             for x in API.words(rel_bga=word, topics=category, ml=word, md='p') if 'tags' in x]
    return [x['word'] for x in words if pos in x['tags']] if pos else words


def trigger(word: str, category: str = '', pos: str = '') -> list:
    """
        Returns list of words that are STRONGLY ASSOCIATED with the 'word'
        Can be filtered further down by passing extra attributes such as category and part of speech
        category: (animal, plant, and etc)
        pos: noun -> n, verb -> v, adj -> adj, adverb -> adv
        by default category and pos are null
    """
    words = [x if pos else x['word']
             for x in API.words(rel_trg=word, ml=word, topics=category, md='p') if 'tags' in x]
    return [x['word'] for x in words if pos in x['tags']] if pos else words


if __name__ == "__main__":
    main()
