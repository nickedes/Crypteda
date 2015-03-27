
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


def schedule(key, iteration, atable, ltable):
    new_key = key
    new_key = new_key[1:] + new_key[:1]
    for k in range(0, len(new_key)):
        i = int(new_key[k], 16)
        #sbox value
        #new_key[k] = sbox1(i)
    new_key[0] ^= rcon(iteration)
    return new_key


def Rijndael_key_schedule(key):
    # temporaray 4-byte
    c = 16
    iteration = 1
    # for i in range(len(key)):
        # key[i] = int(key[i], 16)
    # we need 11 sets of 16 bytes each
    key_i = []
    for k in range(0, len(key)):
        key_i.append(int(key[k], 16))
    while c < 176:
        t = []
        for i in range(4):
            t.append(key[i + c - 4])
        if c % 16 == 0:
            t = schedule(t,iteration)
            iteration += 1
        for i in range(4):
            print(t[i])
            # key_i[c] = key_i[c - 16] ^ t[i]
            c += 1
    return key_i

s = ['EA', '04', '65', '85', '83', '45', '5D', '96',
     '5C', '33', '98', 'B0', 'F0', '2D', 'AD', 'C5']

key = 'ffffffffffffffffffffffffffffffff'
# key = ['f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f']

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

print(Rijndael_key_schedule(key))
