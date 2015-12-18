from hashlib import md5
from Crypto.Cipher import AES

def get_key_and_iv(password, salt, key_length, iv_length):
    a = a_i = ''
    while len(a) < key_length + iv_length:
        a_i = md5(a_i + password + salt).digest()
        a += a_i
    return a[:key_length], a[key_length:key_length+iv_length]

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = get_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)