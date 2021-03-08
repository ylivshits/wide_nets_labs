import socket
import random
from operator import xor

blocksize = 61
control = [0, 1, 2, 4, 8, 16, 32, 64, 128]
def split_blocks(a):
    res = [[]]
    for k in a:
        for i in range(8):
            res[-1].append((k >> i) & 1)
            if len(res[-1]) == blocksize:
                res.append([])

    if (len(res[-1]) == 0):
        res.pop()
    while(len(res[-1]) < blocksize):
        res[-1].append(0)
    return res

def unite_blocks(a):
    res = ''.encode('UTF-8')
    curres = 0
    j = 0
    for cur in a:
        for ind in cur:
            if j == 8:
                res += bytes([curres])
                j = 0
                curres = 0
            curres = (curres | (ind << j))
            j += 1
    if curres != 0 or j <= 8: 
        res += bytes([curres])

    return res

def hamming_code(block):
    res = []
    ind = 0
    for i in block:
        while len(res) == control[ind]:
            res.append(0)
            ind += 1
        res.append(i)

    for i in range(len(res)):
        for bit in range(8):
            if ((i >> bit) & 1):
                res[1 << bit] = (res[1 << bit] ^ res[i])

    return res

cnt_zero = 0
cnt_one = 0
cnt_many = 0

def one_error(a):
    global cnt_zero 
    global cnt_one 
    global cnt_many 
    if (random.randrange(2) == 0):
        cnt_zero += 1
        return a
    a[random.randrange(len(a)-1)+1] ^= 1
    cnt_one += 1
    return a

def many_errors(a, n):
    global cnt_zero 
    global cnt_one 
    global cnt_many 
    if (random.randrange(2) == 0):
        cnt_zero += 1
        return a
    tmp = random.randrange(n)
    tmp += 1
    if (tmp == 1):
        cnt_one += 1
    if (tmp > 1):
        cnt_many += 1
    for i in range(tmp):
        a[random.randrange(len(a)-1)+1] ^= 1
    return a


sock = socket.socket()
sock.connect(('192.168.100.68', 9090))

for test in range(3):
    cnt_zero = 0
    cnt_one = 0
    cnt_many = 0

    if (test == 0):
        print('TEST WITHOUT ERRORS')
    if (test == 1):
        print('TEST WITH SINGLE ERRORS')
    if (test == 2):
        print('TEST WITH MULTIPLE ERRORS')

    mytext = open('/home/alexandr/Desktop/text.txt', 'r', encoding = 'UTF-8').read()
    bar = mytext.encode('UTF-8');
    
    tmp = split_blocks(bar)
    
    for i in range(len(tmp)):
        tmp[i] = hamming_code(tmp[i])

    if (test == 0):
        for i in range(len(tmp)):
            cnt_zero += 1

    if (test == 1):
        for i in range(len(tmp)):
            tmp[i] = one_error(tmp[i])
    
    if (test == 2):
        for i in range(len(tmp)):
            tmp[i] = many_errors(tmp[i], 5)
    

    print('Number of blocks generated with zero mistakes: ', cnt_zero)
    print('Number of blocks generated with one mistake: ', cnt_one)
    print('Number of blocks generated with many mistakes: ', cnt_many)


    bar = unite_blocks(tmp)
    
    sock.send(bar)
    data = sock.recv(8196).decode('UTF-8')
    print(data)




sock.close()
