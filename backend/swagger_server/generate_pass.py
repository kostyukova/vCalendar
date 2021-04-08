import os
import hashlib

# hex() produce 2 digits for every byte
salt = os.urandom(64)
password = 'qwePass!23'
password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, 64)
print('password:{}\npassword hash: {}\nsalt: {}'
    .format(password, password_hash.hex(), salt.hex()))
