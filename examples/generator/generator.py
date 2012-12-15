#-*- coding: utf-8 -*-

import string
import re

al = ' ' + ''.join([chr(ch) for ch in range(ord(u'а'), ord(u'я') + 1)])
print al

def normalize(block):
    block = block.lower()
    block = re.sub('[{0}]'.format(string.punctuation), '', block)
    block = re.sub('[\s]+', ' ', block)
    return block

def encode(block, key):
    out = ''
    for i, ch in enumerate(block):
        out += al[(al.index(ch) + al.index(key[i % len(key)])) % len(al)]
    return out
    
def decode(block, key):
    out = ''
    for i, ch in enumerate(block):
        out += al[(al.index(ch) - al.index(key[i % len(key)])) % len(al)]
    return out
    
block = '''Лавина  книг  обрушилась  на  Монтэга,  когда  он  с  тяжелым  сердцем,
содрогаясь всем  своим существом,  поднимался вверх по крутой лестнице.  Как
нехорошо получилось! Раньше всегда проходило гладко... Все  равно как  снять
нагар со свечи. Первыми являлись полицейские, заклеивали  жертве  рот липким
пластырем и, связав ее, увозили куда-то'''

key = 'свеча'
num = 16

f = open('{0}.txt'.format(num), 'w')
asc = open('{0}.asc'.format(num), 'w')
#print([al.index(ch) for ch in key[:4]])

block = normalize(block)
enc = encode(block, key)
dec = decode(enc, key)
print(dec)
print(num)
f.write(key + '\n\n')
f.write(enc + '\n\n')
f.write(dec + '\n\n')
asc.write(enc)
