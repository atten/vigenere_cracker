#coding: UTF-8
import math

def expectedValue(probabilitiesMap, alphabet):
    d = 0

    for ch in probabilitiesMap:
        d += (alphabet.index(ch) + 1) * probabilitiesMap[ch]

    return d

def indexOfCoincidence(cipher, alphabet):
    counts = {}

    for a in alphabet:
        counts[a] = 0

    for ch in cipher:
        counts[ch] += 1

    index = 0
    for c in counts:
        index += (counts[c] * (counts[c] - 1) * 1.0) / (len(cipher) * (len(cipher) - 1) * 1.0)

    return index

def extractSymbols(str, period, shift=0):
    ret = ""
    for (i, x) in enumerate(str):
        if not (i - shift) % period:
            ret += x

    return ret

def charFrequences(str):
    dict = {}
    for c in str:
        if c in dict:
            dict[c] += 1
        else:
            dict[c] = 1

    for c in dict:
        dict[c] = 1.0 * dict[c] / len(str)

    return dict

def applyGamma(text, gamma, alphabet, uncipher=False):
    ret = ""
    gammaPos = 0

    for ch in text:
        if uncipher:
            ret += alphabet[(alphabet.index(ch) + alphabet.index(gamma[gammaPos])) % len(alphabet)]
        else:
            ret += alphabet[(alphabet.index(ch) - alphabet.index(gamma[gammaPos])) % len(alphabet)]
        gammaPos = (gammaPos + 1) % len(gamma)

    return ret

def addGamma(text, gamma, alphabet):
    return applyGamma(text, gamma, alphabet, uncipher=False)

def substractGamma(text, gamma, alphabet):
    return applyGamma(text, gamma, alphabet, uncipher=True)

def crack(cipher, alphabet, maxGammaLength = 20):
    values = {}

    print "|Cipher| =", len(cipher), "symbols\n"\
          "|Alphabet| =", len(alphabet), "symbols\n"\
          "Max |Gamma| is set to", maxGammaLength, "\n"

    for length in range(1, min(len(cipher) - 1, maxGammaLength) + 1):
        sequence = extractSymbols(cipher, period=length)
        index = indexOfCoincidence(sequence, alphabet)

        if index > 1.0 / len(alphabet) or len(cipher) < 10:
            values[length] = index

        print "Gamma length =", length, "; Index of coincidence =", index

    gammaLengths = [x for x in sorted(values, key=values.get, reverse=True)]
    print "\nMost probable gamma lengths (in descendant order):\n", gammaLengths

    for length in gammaLengths:
        print "\n|Gamma| = %d:" % length

        probableGamma = ""

        for i in range(length):
            print "\tSymbol", i+1, ":"
            group = extractSymbols(cipher, length, i)

            symbols = {}
            previousVal = 0
            for j in range(-1, len(alphabet)):
                val = expectedValue(charFrequences(addGamma(group, alphabet[j], alphabet)), alphabet)
                if j != -1:
                    symbols[alphabet[j]] = abs(val - previousVal)
                    #print "\t", alphabet[j], "=", abs(val - previousVal)
                previousVal = val

            charList = sorted(symbols, key=symbols.get, reverse=True)
            print "\tMost probable characters:", ", ".join(charList), "\n"
            probableGamma += charList[0]

        print "\tApplying gamma '%s': %s..." % (probableGamma, applyGamma(cipher[0:80], probableGamma, alphabet))


cipher   = open(u"G:/Docs/text/Учеба/Криптология/Lab2/Задачи лр №2/5.txt").read().replace("\n", "").decode("UTF-8")
alphabet = open(u"G:/Docs/text/Учеба/Криптология/Lab2/vigenere_cracker/data/alphabet.txt").read().decode("CP1251")
crack(cipher, alphabet, maxGammaLength=20)

#text = u"ему показалось что он вошел в холодный облицованный мрамором склеп после того как зашла лсна непроницаемый мрак ни намека на еалктый серебряным сиянкгм мир за оилом окна плотно закрыты и комната похожа на могилу куда не долетает ни единый звук большого города однако комната не была пуста"
#gamma = u"тмжетожетмжетожгтожетмжетмжетмжетожетмжетмжетмжетмжеткжеткжетмжетмжетмжетмжетмжермжетмжетожетмжетожетмжетмжетмжетмжетмжетмжетожетмжетмжетмжетмжетмжетожетмжетмжетожетожетмжетмжетмжетмжетмжетмжетмжетмжетмжетмжефмжермжетмжетожетмжетмжетмжетмжетмжетожзтожетмжетмжетмжерожетмжетмжетмжетмжетмже"
#print applyGamma(cipher, gamma, alphabet, uncipher=False)