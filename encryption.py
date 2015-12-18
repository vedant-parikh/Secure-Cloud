from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random

def get_key_and_iv(password, salt, key_length, iv_length):
    a = a_i = ''
    while len(a) < key_length + iv_length:
        a_i = md5(a_i + password + salt).digest()
        a += a_i
    return a[:key_length], a[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = get_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))
