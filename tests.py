#coding: UTF-8

import vigenere_cracker
import time


text = u'''ему показалось что он вошел в холодный облицованный мрамором склеп после того как зашла луна непроницаемый
       мрак ни намека на залитый серебряным сиянием мир за окном окна плотно закрыты и комната похожа на могилу куда не
       долетает ни единый звук большого города однако комната не была пуста'''.replace('\n', '')

alphabet = open(u"data/alphabet.txt").read().decode("CP1251")

class Gag:                                           # класс для пустого текстового вывода минуя консоль
    def write(self, string):
        pass


def basicTest():
    global text, alphabet
    gamma = u'след'
    start = time.clock()
    cipher = vigenere_cracker.applyGamma(text, gamma, alphabet)
    vigenere_cracker.crack(cipher, alphabet)
    print 'time = %fs' % (time.clock() - start)


def timeTest():
    global text, alphabet
    gammas = (u'ы',
              u'му',
              u'дом',
              u'след',
              u'бочка',
              u'тишина',
              u'молоток',
              u'бензобак',
              u'бомбардир',
              u'бронежилет',
              u'полуавтомат',
              u'спецоперация',
              u'автопогрузчик',
              u'реструктурация',
              u'металлочерепица')

    gammaRange = range(1, len(gammas[-1]) + 1)

    print 'Starting Time Test for different Gamma lengths [%d...%d]:' % (len(gammas[0]), len(gammas[-1]))
    for g in gammas:
        start = time.clock()
        cipher = vigenere_cracker.applyGamma(text, g, alphabet)
        vigenere_cracker.crack(cipher, alphabet, len(g), output=Gag())
        elapsed1 = time.clock() - start
        start = time.clock()
        vigenere_cracker.crack(cipher, alphabet, gammaRange, output=Gag())
        elapsed2 = time.clock() - start
        print '|Gamma| = %d ; Pure time = %fs ; Full time = %fs' % (len(g), elapsed1, elapsed2)

    print 'Done.'


def similarityPercent(str1, str2):
    d = 0
    maxLen = max(len(str1), len(str2))
    minLen = min(len(str1), len(str2))

    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            d += 1

    return (1.0 * minLen - d) / maxLen


def reliabilityTest():
    global text, alphabet

    gamma = u'двигатель'

    print 'Starting Reliability Test for Ciphertexts with different lengths:'
    print '|Gamma| = %d:\n' % len(gamma)

    for l in range(len(text), 0, -10):
        start = time.clock()
        cipher = vigenere_cracker.applyGamma(text[:l], gamma, alphabet)
        results = vigenere_cracker.crack(cipher, alphabet, keyLength=range(1, len(gamma)+1), output=Gag())
        reliability = 0
        reliableGamma = ''

        for g, t in results:
            k = similarityPercent(g, gamma)
            if k > reliability:
                reliableGamma = g
                reliability = k

        print 'Cipher length = %d ; Time = %fs ; Gamma = "%s" ; Reliability = %d%%' % (len(cipher), time.clock() - start, reliableGamma, 100 * reliability)

    print 'Done.'


def test():
    basicTest()
    timeTest()
    reliabilityTest()

test()