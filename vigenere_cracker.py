#coding: UTF-8
from __future__ import print_function
import sys

def frequences(str):
    """
    Возвращает словарь, состоящий из частот появления отдельных символов в данной строке.

    Аргументы:
        str - строка для анализа.
    """
    dict = {}
    for c in str:
        if c in dict:
            dict[c] += 1
        else:
            dict[c] = 1

    for c in dict:
        dict[c] = 1.0 * dict[c] / len(str)

    return dict

def entropy(string, alphabet):
    """
    Возвращает мат. ожидание текста.

    Аргументы:
        string - анализируемая строка
        alphabet - коллекция символов алфавита
    """
    freq = frequences(string)
    e = 0

    for ch in freq:
        e += (alphabet.index(ch) + 1) * freq[ch]

    return e

def indexOfCoincidence(text, alphabet):
    """
    Возвращает индекс совпадения (вероятность совпадения двух произвольных символов в тексте).
    Мин. значение: 1 / len(text)       (для случайного текста)
    Макс. значение: 1

    Аргументы:
        text - текст, на основе которого вычисляется индекс
        alphabet - коллекция символов, которая включает все символы текста
    """
    if len(text) == 1:
        return 0

    counts = {}
    for a in alphabet:
        counts[a] = 0

    for ch in text:
        counts[ch] += 1

    index = 0
    for c in counts:
        index += (counts[c] * (counts[c] - 1) * 1.0) / (len(text) * (len(text) - 1) * 1.0)

    return index

def extractSymbols(str, period, shift=0):
    """
    Возвращает строку, состоящую из каждого i-го символа исходной строки.

    Аргументы:
        str - исходная строка
        period - период повторений
        shift - порядковый номер символа, с которого начнется отсчет.
    """
    ret = ""
    i = shift
    while i < len(str):
        ret += str[i]
        i += period

    return ret

def removeIllegalChars(text, alphabet):
    arr = set(text) - set(alphabet)
    if not len(arr):
        return text

    print ('Warning: text contains %d characters that are not found in the alphabet:\n\t(%s). Ignore them.\n'\
            % (len(arr), ', '.join(arr)))

    for c in arr:
        text = text.replace(c, '')

    return text

def applyGamma(text, gamma, alphabet, decode=False):
    """
    Складывает гамму с исходным текстом и возвращает результат. Является реализацией шифра Виженера.

    Аргументы:
        text - исходный текст
        gamma - ключ шифрования
        alphabet - список символов, на  основе которого применяется криптографическое преобразование
        decode - лог. значение; True означает сложение гаммы из текстом, False - вычитание.
    """
    ret = ""

    for i, ch in enumerate(text):
        if decode:
            ret += alphabet[(alphabet.index(ch) + len(alphabet) - alphabet.index(gamma[i % len(gamma)])) % len(alphabet)]
        else:
            ret += alphabet[(alphabet.index(ch) + alphabet.index(gamma[i % len(gamma)])) % len(alphabet)]

    return ret

def crack(cipher, alphabet, frequencyTable, keyLength = range(1, 10), variants = 3, output = sys.stdout, moreInfo = True):
    if not len(cipher):
        return

    cipher = removeIllegalChars(cipher, alphabet)

    if isinstance(keyLength, int):
        keyLength = [keyLength]

    if not len(frequencyTable):
        frequencyTable = alphabet

    print ("|Cipher| =", len(cipher), "symbols\n"\
          "|Alphabet| =", len(alphabet), "symbols\n"\
          "Assumed |Gamma| =", keyLength, "\n", file=output)

    indexes = {}
    for length in keyLength:                                # перебираем длины гаммы
        index = 0                                           # индекс совпадений
        for i in range(length):                             # считаем для каждой подгруппы симовлов
            sequence = extractSymbols(cipher, period=length, shift=i)
            index += indexOfCoincidence(sequence, alphabet)

        index /= 1.0 * length                               # находим средний индекс для всех подгрупп
        indexes[length] = index

        if (moreInfo): print ("Gamma length =", length, "; Index of coincidence =", index, file=output)

    minIndex = 1.9 / (len(alphabet))                    # допустимый минимальный индекс совпадения
    if (moreInfo): print ('Minimal allowed index for this alphabet = %f' % minIndex, file=output)

    gammaLengths = []
    for l in indexes:                                       # выбираем только те длины гаммы, индексы совпадений
        if indexes[l] > minIndex: gammaLengths.append(l)    # для которых выше допустимого
                                                            # опционально: останавливаемся на минимальной длине гаммы

    if not len(gammaLengths):                               # если ни одна длина не подходит, используем ВСЕ
        gammaLengths = indexes.keys()
    elif len(gammaLengths) == len(indexes):                 # если все длины подходят, используем [1]
        gammaLengths = [1]

    print ("\nMost probable gamma length:\n", gammaLengths, file=output)

    results = []
    for length in gammaLengths:
        print ("\n|Gamma| = %d:" % length, file=output)

        probableGamma = []

        for l in range(length):
            group = extractSymbols(cipher, length, l)

            symbols = {}
            for ch in alphabet:
                val = entropy(applyGamma(group, ch, alphabet, True), frequencyTable)
                symbols[ch] = val
                #print ("\tEntropy of group for gamma =", ch, ":", val, file=output)

            charList = sorted(symbols, key=symbols.get)
            if moreInfo: print ("\tMost probable candidates for symbol", l+1, ":", ", ".join(charList), file=output)
            probableGamma.append(charList)                   # добавляем массив всех символов-кандидатов

        variantsCount = 2**(len(probableGamma))              # выведем два варианта на каждую букву гаммы
        textVariants = {}                                    # словарь текстов по ключу энтропии
        for variant in range(variantsCount):
            gamma = ""
            for index in range(len(probableGamma)):
                gamma += probableGamma[index][(variant >> index) % 2]

            result = applyGamma(cipher, gamma, alphabet, True)
            e = entropy(result, alphabet)
            textVariants[e] = (gamma, result[:80])
            results.append(textVariants[e])

        print ("\n\tMost probable text variants:", file=output)

        for e in sorted(textVariants.keys())[:variants]:   # выберем тексты с наименьшей энтропией
            print ("\tGamma ='%s'; text = %s..." % textVariants[e], file=output)

    return results
