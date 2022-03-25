from json import dumps, loads


def main():
    filename = 'temp.txt'
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readlines()
    data = [x.strip() for x in data]

    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(len(data)):
            f.write(f'"{data[i]}"{"," if i != len(data) - 1 else ""}\n')


if __name__ == "__main__":
    main()
