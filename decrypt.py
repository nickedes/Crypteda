from tables import *

def inv_substi(s, inv_sbox):
    substi = []
    i = 0
    for k in range(len(s)):
        substi.append([])

    for k in range(len(s)):
        for i in range(len(s[k])):
            if len(s[k][i]) == 1:
                s[k][i] = '0' + s[k][i]
            substi[k].append(
                inv_sbox[int(s[k][i][0], 16)][int(s[k][i][1], 16)])
    return substi


def multiply(y, x):

    if y == 9:
        return mul_9[x]
    elif y == 11:
        return mul_11[x]
    elif y == 13:
        return mul_13[x]
    elif y == 14:
        return mul_14[x]


def inv_mixcolumns(s):

    fixed_matrix = [['0e', '0b', '0d', '09'], ['09', '0e', '0b', '0d'], [
        '0d', '09', '0e', '0b'], ['0b', '0d', '09', '0e']]

    for k in range(len(s)):
        for j in range(len(s[k])):
            s[k][j] = int(s[k][j], 16)

    for k in range(len(fixed_matrix)):
        for j in range(len(fixed_matrix[k])):
            fixed_matrix[k][j] = int(fixed_matrix[k][j], 16)

    c = [[0 for row in range(len(s))] for col in range(len(fixed_matrix))]

    for i in range(len(s)):
        for j in range(len(fixed_matrix)):
            for k in range(len(s)):
                c[i][j] ^= int(multiply(fixed_matrix[i][k], s[k][j]), 16)

    for k in range(len(c)):
        for j in range(len(c[k])):
            c[k][j] = hex(c[k][j])[2:]
    return c


def inv_shiftrows(s):
    shifted_s = []

    for i in range(len(s)):
        shifted_s.append(s[i][len(s) - i:] + s[i][:len(s) - i])

    return shifted_s


def gen(key):
    keys = {}
    first_key = []
    for k in range(0, int(len(key) / 8)):
        first_key.append([])
    for i in range(len(key)):
        first_key[int(i / 8)].append(key[i])

    # ['f','a','b','b','1','3','c','d'] -> ['fa','bb','13','cd']
    for i in range(len(first_key)):
        join_by_2 = []
        for j in range(0, len(first_key[i]), 2):
            join_by_2.append(''.join(first_key[i][j:j + 2]))
        first_key[i] = join_by_2
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


cipher_text = [['84', '27', '3f', '5b'], ['df', '9d', 'ff', '31'],
               ['25', '73', 'a2', '7e'], ['97', '6e', 'ad', '82']]

key = ['d', '6', 'd', '3', 'a', '3', '9', '7', '6', '4', 'e', '8', '9', '2',
       '0', '4', '0', '8', '2', 'e', 'b', '5', 'd', 'd', '2', 'b', '8', 'e',
       'd', '5', '7', '6']

all_key = gen(key)
key_no = 40
print("Cipher text:", cipher_text)
print()

last_key = word_to_key([all_key[key_no], all_key[key_no + 1],
                        all_key[key_no + 2], all_key[key_no + 3]])
cipher_text = inv_substi(inv_shiftrows(add_round_key(cipher_text, last_key)), inv_sbox)
print("Round 1:", cipher_text)

round = 2
while key_no > 4:
    key_no -= 4
    key = word_to_key([all_key[key_no], all_key[key_no + 1],
                       all_key[key_no + 2], all_key[key_no + 3]])
    cipher_text = inv_substi(inv_shiftrows(inv_mixcolumns(add_round_key(cipher_text, key))), inv_sbox)
    print("Round %d:" % round, cipher_text)
    round += 1

key_no -= 4
key = word_to_key([all_key[key_no], all_key[key_no + 1],
                   all_key[key_no + 2], all_key[key_no + 3]])
decypted_text = add_round_key(cipher_text, key)

print()
print("Round 11 (Decrypted text):", decypted_text)
