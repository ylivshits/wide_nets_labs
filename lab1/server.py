import socket

control = [0, 1, 2, 4, 8, 16, 32, 64, 128]

def split_bytes(a):
	res = [[]]
	for byte in a:
		for bit in range(8):
			if len(res[-1]) == 69:
				res.append([])
			res[-1].append((byte >> bit) & 1)
	if len(res[-1]) == 0:
		res.pop()
	while len(res[-1]) < 69:
		res[-1].append(0)
	return res

def decode(a):
	for i in range(len(a)):
		if i in control:
			continue
		for j in range(7):
			a[pow(2,j)] ^= ((i >> j) & 1) * a[i]
	return a

def search_ind_error(a):
	res = 0
	for i in control:
		if i > len(a):
			break
		res ^= (i * a[i])
	return res

num_correct_words = 0
num_1_error_words = 0
num_many_error_words = 0

def hamming_code(a):
	global num_correct_words
	global num_1_error_words
	global num_many_error_words
	a[0] = 0
	b = a.copy()
	a = decode(a)
	res = search_ind_error(a)
	if res >= len(a):
		num_many_error_words += 1
		return a
	if res != 0:
		b[res] ^= 1
		b = decode(b)
		res = search_ind_error(b)
		if res != 0:
			num_many_error_words += 1
		else:
			num_1_error_words += 1
		return b
	else:
		num_correct_words += 1
		return a
	
def delete_control_bits(a):
	res = []
	for i in range(len(a)):
		if i in control:
			continue
		res.append(a[i])
	return res

def unite_blocks(a):
	res = ''.encode('UTF-8')
	j = 0
	curres = 0
	for i in a:
		for bit in i:
			if j == 8:
				res += bytes([curres])
				j = 0
				curres = 0
			curres |= (bit << j)	
			j += 1
	if curres != 0 or j <= 8:
		res += bytes([curres])
	return res

		
sock = socket.socket()

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()
print('connected', addr)
conn.settimeout(1)

for test in range(3):
	num_correct_words = 0
	num_1_error_words = 0
	num_many_error_words = 0
	data = ''.encode('UTF-8')

	while True:
		try:
			curres = conn.recv(8196)
			data += curres
		except:
			break
		
	data = split_bytes(data)
	for i in range(len(data)):
		data[i] = hamming_code(data[i])
		data[i] = delete_control_bits(data[i])
	data = unite_blocks(data)

	try:
		print(data.decode('UTF-8'))
	except:
		print('Could not decode because of multiple errors')
	
	string = 'Try number ' + str(test + 1) + '\n'
	string += 'Number of correct words = ' + str(num_correct_words) + '\n'
	string += 'Number of words with one error = ' + str(num_1_error_words) + '\n'
	string += 'Number of words with many errors = ' + str(num_many_error_words) + '\n'
	string += 'Number of correct words TOTAL = ' + str(num_correct_words + num_1_error_words)

	conn.send(string.encode('UTF-8'))

conn.close()