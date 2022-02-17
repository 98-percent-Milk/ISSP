from nltk.corpus import wordnet as wn
import json


def main():
    with open('textures.json', 'r') as f:
        data = json.load(f)

    textures = {}
    for texture in data['texture']:
        lex = set(x.lexname() for x in wn.synsets(texture.lower()))
        textures[texture.lower()] = lex

    with open('textures.txt', 'w') as f:
        for k, v in textures.items():
            f.write(f"{k:<10}:{v}\n")


def get_colors():
    colors = ['red', 'orange', 'yellow', 'green', 'cyan',
              'blue', 'magenta', 'purple', 'white', 'black', 'grey',
              'silver', 'pink', 'maroon', 'brown', 'beige', 'tan',
              'peach', 'lime', 'olive', 'turquoise', 'teal', 'navy_blue',
              'indigo', 'violet']
    filename = 'colors.txt'
    lexes = {}

    for color in colors:
        lex = set(x.lexname() for x in wn.synsets(color))
        lexes[color] = lex
    print(lexes)

    with open(filename, 'w') as f:
        for k, v in lexes.items():
            f.write(f"{k:<10}:{v}\n")


if __name__ == "__main__":
    main()

# colors = ['red', 'orange', 'yellow', 'green', 'cyan',
#           'blue', 'magenta', 'purple', 'white', 'black', 'grey',
#           'silver', 'pink', 'maroon', 'brown', 'beige', 'tan',
#           'peach', 'lime', 'olive', 'turquoise', 'teal', 'navy_blue',
#           'indigo', 'violet']
