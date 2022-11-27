from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from jsonclass import Json
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP, AES
from hashlib import sha256
import base64


def check_header(header):
    try:
        password = header['PASSWORD']
        h = header_check(password)
        with open('header_check.txt','r') as file:
            decrypt = h.decrypt(file.read())
        return decrypt == 'Passed the Password Check'
    except:
        return False
        


class header_check:
    def __init__(self,key) -> None:

        self.bs = AES.block_size
        self.key =  sha256(key.encode('utf8')).hexdigest().encode('utf8')[32:]
    

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode('LATIN-1')))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


    
    def write_check(self,raw):
        en_text = self.encrypt(raw)
        with open('header_check.txt','wb') as file:
            file.write(en_text)

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
if __name__ == '__main__':
    password = 'TvtQ23L5vJqJ3x'
    # d = header_check(password)
    # d.write_check('Passed the Password Check')
    print(check_header(password))
