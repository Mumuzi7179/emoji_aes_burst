# -*- codeing = utf-8 -*-
# @Time : 2021/12/28 17:53
# @Author : Mumuzi
# @File : burst_emoji_aes.py
# @Software : PyCharm

'''
其实和emoji-aes没啥关系，就替换成base64之后再爆破而已...
emmmm当然直接去调js也行，只是我不会
脚本中重要部分也是github有的，所以这题很简单
扒源码的时候注意到他是先小写再大写，正常base64表是先大写再小写的
'''

from tqdm import tqdm
from Crypto.Cipher import AES
import base64
from hashlib import md5
import string
import itertools

emojisInit = ["🍎", "🍌", "🏎", "🚪", "👁", "👣", "😀", "🖐", "ℹ", "😂", "🥋", "✉", "🚹", "🌉", "👌", "🍍", "👑", "👉", "🎤", "🚰", "☂", "🐍", "💧", "✖", "☀", "🦓", "🏹", "🎈", "😎", "🎅", "🐘", "🌿", "🌏", "🌪", "☃", "🍵", "🍴", "🚨", "📮", "🕹", "📂", "🛩", "⌨", "🔄", "🔬", "🐅", "🙃", "🐎", "🌊", "🚫", "❓", "⏩", "😁", "😆", "💵", "🤣", "☺", "😊", "😇", "😡", "🎃", "😍", "✅", "🔪", "🗒"]
table = string.ascii_lowercase+string.ascii_uppercase+string.digits+'+/='
table = list(table)

def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]

def decrypt(emo, passphrase):
    #https://my.oschina.net/u/3021599/blog/3134709
    bs64 = ''
    for i in emo:
        bs64 += table[emojisInit.index(i)]
    encrypted = base64.b64decode(bs64)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))

if __name__ == '__main__':
    TABLE = string.ascii_lowercase+string.digits
    emoji_enc = input('input your emoji_enc:')
    for i in tqdm(itertools.product(''.join(i for i in TABLE), repeat= 6)):
        passphrase = str(''.join(i)).encode('utf-8')
        result = decrypt(emoji_enc,passphrase)
        if(b'flag' in result):
            print('text is :',result,'and key is :',passphrase)
