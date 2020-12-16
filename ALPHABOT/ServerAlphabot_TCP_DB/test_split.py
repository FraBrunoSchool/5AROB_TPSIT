import re


def main():
    data = 'B50R90F600L90F400'
    """
    B 50  R 90  F 600  L 90  F400
    [(b, 50), (r, 90), (f, 600), (l, 90), (f, 400)]
   """
    lista_potenze = re.split('B|R|F|L', data)
    print(lista_potenze)
    lista_potenze.pop(0)
    regex = ''
    for index, el in enumerate(lista_potenze):
        if index == len(lista_potenze) - 1:
            regex += el
        else:
            regex += el + '|'
    lista_direzioni = re.split(regex, data)
    lista_direzioni.pop(-1)
    comandi = []
    for index, el in enumerate(lista_potenze): comandi.append((lista_direzioni[index], int(el)))
    print(comandi)


if __name__ == '__main__':
    main()
