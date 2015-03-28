
def substitute(s, sbox):
    substi = []
    i = 0
    for k in range(0, int(len(s) / 4)):
        substi.append([])

    for k in range(len(s)):
        substi[i].append(sbox[int(s[k][0], 16)][int(s[k][1], 16)])
        if (k + 1) % 4 == 0:
            i = i + 1
    return substi

def gen(key):
    keys = {}
    first_key = []
    for k in range(0, int(len(key) / 8)):
        first_key.append([])
    for i in range(len(key)):
        first_key[int(i/8)].append(key[i])
    
    # ['f','a','b','b','1','3','c','d'] -> ['fa','bb','13','cd']
    for i in range(len(first_key)):
        join_by_2 = []
        for j in range(0,len(first_key[i]),2):
            join_by_2.append(''.join(first_key[i][j:j+2]))
        first_key[i]=join_by_2
    w = []
    for i in range(44):
        w.append([])
    # 4 words
    for i in range(len(first_key)):
        w[i]=first_key[i]
    # no. of words
    i = 4
    # until no. of words = 44
    while i<44:
        temp = w[i-1]
        if i%4 == 0:
            temp = sub(rotword(temp))
            #^ rcon(i/4)
            temp[3] = hex(int(temp[3],16) ^ rcon(int(i/4)))[2:]
        for j in range(len(temp)):
            temp[j] = hex(int(temp[j],16) ^ int(w[i-4][j],16))[2:]
        print(temp)
        w[i]=temp
        i+=1
    return w    

def rotword(word):
    # ['fa','bb','13','cd'] -> ['bb','13','cd','fa']  
    return word[1:]+word[:1]

def sub(word):
    # ['fa','bb','13','cd'] -> sbox values
    for i in range(len(word)):
        if len(word[i]) == 1:
            word[i] ='0'+word[i]
        word[i] = sbox[int(word[i][0], 16)][int(word[i][1], 16)]
    return word

def shiftrows(s):
    shifted_s = []

    # for k in range(0, int(len(s) / 4)):
    # shifted_s.append([])

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


s = ['EA', '04', '65', '85', '83', '45', '5D', '96',
     '5C', '33', '98', 'B0', 'F0', '2D', 'AD', 'C5']

# key = 'ffffffffffffffffffffffffffffffff'
key = ['f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f']
# key = ['ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff',
       # 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff']
key1 = ['d','6','d','3','a','3','9','7','6','4','e','8','9','2','0','4','0','8','2','e','b','5','d','d','2','b','8','e','d','5','7','6']
sbox = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5',
         '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
        ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0',
         'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
        ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc',
         '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
        ['04', 'c7', '23', 'c3', '18', '96', '05', '9a',
         '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
        ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0',
         '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
        ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b',
         '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
        ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85',
         '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
        ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5',
         'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
        ['cd', '0c', '13', 'ec', '5f', '97', '44', '17',
         'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
        ['60', '81', '4f', 'dc', '22', '2a', '90', '88',
         '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
        ['e0', '32', '3a', '0a', '49', '06', '24', '5c',
         'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
        ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9',
         '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
        ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6',
         'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
        ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e',
         '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
        ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94',
         '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
        ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68',
         '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]


# print(s, "\n", sbox)

# print(substitute(s, sbox))

new_s = substitute(s, sbox)

print(shiftrows(new_s))

shift_rows = shiftrows(new_s)

print(mixcolumns(shift_rows))

print(rcon(1), rcon(2), rcon(10))

# print(Rijndael_key_schedule(key))
# print(gen(key))

# print(rotword(['fa','bb','13','cd

print(gen(key1))