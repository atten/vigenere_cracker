#coding: UTF-8

import vigenere_cracker as crypto
import time


text = u'''ему показалось что он вошел в холодный облицованный мрамором склеп после того как зашла луна непроницаемый
       мрак ни намека на залитый серебряным сиянием мир за окном окна плотно закрыты и комната похожа на могилу куда не
       долетает ни единый звук большого города однако комната не была пуста'''.replace('\n', '')

alphabet = u' абвгдежзийклмнопрстуфхцчшщъыьэюя'
frequencyTable = u' оаеинтрслвкпмудяыьзбгйчюхжшцщфэъ'

class Gag:                                           # класс для пустого текстового вывода минуя консоль
    def write(self, string):
        pass


def basicTest():
    global text, alphabet
    gamma = u'ссрс'
    start = time.clock()
    cipher = crypto.applyGamma(text, gamma, alphabet)
    crypto.crack(cipher, alphabet, frequencyTable, variants=3, moreInfo=True)
    print 'time = %fs' % (time.clock() - start)


def speedTest():
    global text, alphabet, frequencyTable
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
             u'реструктурация')

    gammaRange = range(1, len(gammas[-1]) + 1)

    print 'Starting Time Test for different Gamma lengths [%d...%d]:' % (len(gammas[0]), len(gammas[-1]))
    for g in gammas:
        start = time.clock()
        cipher = crypto.applyGamma(text, g, alphabet)
        crypto.crack(cipher, alphabet, frequencyTable, len(g), output=Gag())
        elapsed1 = time.clock() - start
        start = time.clock()
        crypto.crack(cipher, alphabet, frequencyTable, gammaRange, output=Gag())
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
    global text, alphabet, frequencyTable

    gamma = u'йцукенгшщзх'

    print 'Starting Reliability Test for Ciphertexts with different lengths:'
    print '|Gamma| = %d:\n' % len(gamma)

    for l in range(len(text), 0, -10):
        start = time.clock()
        cipher = crypto.applyGamma(text[:l], gamma, alphabet)
        results = crypto.crack(cipher, alphabet, frequencyTable, keyLength=range(1, len(gamma)+1), output=Gag())
        reliability = 0
        reliableGamma = ''

        for g, t in results:
            k = similarityPercent(g, gamma)
            if k > reliability:
                reliableGamma = g
                reliability = k

        print 'Cipher length = %d ; Time = %fs ; Gamma = "%s" ; Reliability = %d%%' % (len(cipher), time.clock() - start, reliableGamma, 100 * reliability)

    print 'Done.'


def massiveTest():
    start = time.clock()
    print "<html><body>"
    for i in range(1, 17):
        print '<center><big><b>----------'
        print "VARIANT %d" % i
        print '----------</b></big></center>\n'
        cipher = open(u"examples/cipher/%d.txt" % i).read().decode("UTF-8").replace('\n', '')
        crypto.crack(cipher, alphabet, frequencyTable, moreInfo=False)

    print "</body></html>"
    print 'time = %fs' % (time.clock() - start)


def test():
    basicTest()
    #speedTest()
    #reliabilityTest()
    #massiveTest()

test()

