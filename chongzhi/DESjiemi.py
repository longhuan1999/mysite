# 这里使用pycrypto‎demo库
# 安装方法 pip install pycrypto‎demo

from Crypto.Cipher import DES
import base64


class PrpCrypt(object):

    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = DES.MODE_CBC

    # 加密函数，如果text不足8位就用空格补足为8位，
    # 如果大于8当时不是8的倍数，那就补足为8的倍数。
    def encrypt(self, text):
        text = text.encode('utf-8')
        cryptor = DES.new(self.key, self.mode, b'00000000')
        # 这里密钥key 长度必须为8（DES-128）,
        # 24（DES-192）,或者32 （DES-256）Bytes 长度
        # 目前DES-128 足够目前使用
        length = 8
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            # text = text + ('\0' * add)
            text = text + ('\0' * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            # text = text + ('\0' * add)
            text = text + ('\0' * add).encode('utf-8')
        self.ciphertext = cryptor.encrypt(text)
        #self.ciphertext = base64.b64encode(self.ciphertext)
        return self.ciphertext

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = DES.new(self.key, self.mode, b'00000000')
        #text = base64.b64decode(text)
        plain_text = cryptor.decrypt(text)
        # return plain_text.rstrip('\0')
        return bytes.decode(plain_text).rstrip('\0')

