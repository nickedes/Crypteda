from tables import *


def substitute(s, sbox):
    substi = []
    i = 0
    for k in range(len(s)):
        substi.append([])

    for k in range(len(s)):
        for i in range(len(s[k])):
            if len(s[k][i]) == 1:
                s[k][i] = '0' + s[k][i]
            substi[k].append(sbox[int(s[k][i][0], 16)][int(s[k][i][1], 16)])
    return substi


def gen(key):
    keys = {}
    first_key = key

    w = []
    for i in range(44):
        w.append([])

    # 4 words
    for i in range(len(first_key)):
        for j in range(len(first_key[i])):
            w[j].append(first_key[i][j])
        keys[i] = w[i]

    # no. of words
    i = 4

    # until no. of words = 44
    while i < 44:
        temp = []
        for x in w[i - 1]:
            temp.append(x)
        if i % 4 == 0:
            temp = sub(rotword(temp))
            #^ rcon(i/4)
            temp[0] = hex(int(temp[0], 16) ^ rcon(int(i / 4)))[2:]
        for j in range(len(temp)):
            temp[j] = hex(int(temp[j], 16) ^ int(w[i - 4][j], 16))[2:]
        w[i] = temp
        keys[i] = w[i]
        i += 1
    return keys


def rotword(word):
    # ['fa','bb','13','cd'] -> ['bb','13','cd','fa']
    return word[1:] + word[:1]


def sub(word):
    # ['fa','bb','13','cd'] -> sbox values
    for i in range(len(word)):
        if len(word[i]) == 1:
            word[i] = '0' + word[i]
        word[i] = sbox[int(word[i][0], 16)][int(word[i][1], 16)]
    return word


def shiftrows(s):
    shifted_s = []
    for i in range(len(s)):
        shifted_s.append(s[i][i:] + s[i][:i])

    return shifted_s


def multiply(x, y):

    initial_y = y

    if x == 1:
        return y
    else:
        y = y << 1
        if y > 255:
            y ^= int('11B', 16)
        if x == 3:
            y ^= initial_y
    return y


def mixcolumns(s):

    fixed_matrix = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]

    for k in range(len(s)):
        for j in range(len(s[k])):
            s[k][j] = int(s[k][j], 16)

    c = [[0 for row in range(len(s))] for col in range(len(fixed_matrix))]

    for i in range(len(s)):
        for j in range(len(fixed_matrix)):
            for k in range(len(s)):
                c[i][j] ^= multiply(fixed_matrix[i][k], s[k][j])

    for k in range(len(c)):
        for j in range(len(c[k])):
            c[k][j] = hex(c[k][j])[2:]
    return c


def rcon(i):
    rcon_i = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    return rcon_i[i]


def word_to_key(words):
    key = []
    for i in range(len(words)):
        key.append([])
    for i in range(len(words)):
        for j in range(len(words[i])):
            key[i].append(words[j][i])
    return key


def add_round_key(state, key):
    for i in range(len(key)):
        for j in range(len(key[i])):

            key[i][j] = hex(
                int(key[i][j], 16) ^ int(state[i][j], 16))[2:]
    return key

s = [['f3', 'cf', '4d', '15'], ['bf', '4b', 'fb', 'a6'],
     ['8b', 'e2', '52', '58'], ['12', 'ab', '4b', 'b8']]

key = ['d', '6', 'd', '3', 'a', '3', '9', '7', '6', '4', 'e', '8', '9', '2',
       '0', '4', '0', '8', '2', 'e', 'b', '5', 'd', 'd', '2', 'b', '8', 'e',
       'd', '5', '7', '6']

print("Plain text:", s)
print()

all_key = gen(key)
key = word_to_key([all_key[0], all_key[1], all_key[2], all_key[3]])
key_no = 4
s = add_round_key(s, key)
print("Round 1", s)

round = 2
while round < 11:
    round_text = mixcolumns(shiftrows(substitute(s, sbox)))
    key = (word_to_key([all_key[key_no], all_key[key_no + 1], all_key[key_no + 2], all_key[key_no + 3]]))
    s = add_round_key(round_text, key)
    print("Round %d" % round, s)

    key_no += 4
    round += 1

last_round = shiftrows(substitute(s, sbox))
last_key = (word_to_key([all_key[key_no], all_key[key_no + 1], all_key[key_no + 2], all_key[key_no + 3]]))
encrypted_text = add_round_key(last_round, last_key)
print()
print("Round 11 (Encrypted Text): ", encrypted_text)
