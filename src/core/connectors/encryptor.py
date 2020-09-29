import os
import base64
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import logging
from src.settings import log_config


logger = logging.getLogger(__name__)


def aes_encrypt_pass(encrypt_str, mode='decrypt'):
    """
    This function encrypts and decrypt a string using AES
    Syntax: encryption mode [encrypt or decrypt], String to encrypt or decrypt
    """
    user_home = os.environ['HOME']
    pass_key = os.environ['KEY']
    salt_key = open(user_home + '/.peanuts').read()
    pass_key = "{}{}".format(pass_key, salt_key).encode('utf8')

    class AESCipher(object):

        def __init__(self, key):
            self.bs = 32
            self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

        @staticmethod
        def str_to_bytes(data):
            u_type = type(b''.decode('utf8'))
            if isinstance(data, u_type):
                return data.encode('utf8')
            return data

        def _pad(self, s):
            return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

        @staticmethod
        def _unpad(s):
            return s[:-ord(s[len(s)-1:])]

        def encrypt(self, raw):
            raw = self._pad(AESCipher.str_to_bytes(raw))
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf8')

        def decrypt(self, enc):
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf8')

    secret = hashlib.sha256(pass_key).digest()
    aes_cipher = AESCipher(secret)

    if mode == 'encrypt':
        encrypted = aes_cipher.encrypt(encrypt_str)
        logger.debug("password encrypted successfully")
        return encrypted

    if mode == 'decrypt':
        decrypted = aes_cipher.decrypt(encrypt_str)
        logger.debug("password decrypted successfully")
        return decrypted
