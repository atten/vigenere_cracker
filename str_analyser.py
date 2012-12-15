#coding: UTF-8
from __future__ import print_function
import encoding_detector
import sys


nonPrintChars = [chr(i) for i in range(32)]

def charCount(string, counts, skip, caseSensitive = False):
    for c in string:
        if c in skip:
            continue

        if not caseSensitive:
            c = c.lower()

        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1

    return counts


def blockRead(file, bufferSize):
    while True:
        buf = file.read(bufferSize)
        if not len(buf):
            return
        yield buf


def analyse(filenames, caseSensitive = False, skip = [], currentStats = None, output = sys.stdout):
    if isinstance(filenames, str):
        filenames = [filenames]

    size = 0
    counts = {}
    
    if not isinstance(skip, list):
	skip = list(skip)
	
    skip += nonPrintChars
    
    if currentStats:
        counts = currentStats

    for file in filenames:
        text = open(file).read()
        encoding = encoding_detector.get_codepage(text)
        if len(encoding):text = text.decode(encoding)
        size += len(text)
        charCount(text, counts, skip, caseSensitive)

    if not len(filenames):
        return

    print ('Files: %d' % len(filenames), file=output)
    print ('Total chars: %d' % size, file=output)
    print ('Alphabet:\n%s\n' % ''.join(sorted(counts.keys())), file=output)
    print ('Frequency list:\n%s\n' % ''.join(sorted(counts, key=counts.get, reverse=True)), file=output)
    #print ('Counts:\n', counts, file=output)

    return counts
