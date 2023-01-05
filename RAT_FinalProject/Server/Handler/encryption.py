import hashlib
import os
import easygui
import win32api
from easygui import multpasswordbox
from Crypto.Cipher import AES



class EncryptionHandler:
    def __init__(self):
        self.password = ""

    def password_box(self):
        text = "Login access"
        title = "Login access"
        fields = ["Password"]
        output = multpasswordbox(text, title, fields)
        if output:
            self.password = output[0].encode()
            return output[0].encode()
        else:
            win32api.MessageBox(0, 'Error', 'Password field was not filled')
            return None

    """def encrypt(self, key, data):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return [cipher.nonce, tag, ciphertext]

    def decrypt(self, key, nonce, tag, ciphertext):
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data"""

    def encrypt(self, data):
        encoded_data = data.encode()
        salt = os.urandom(32)

        key = hashlib.scrypt(self.password, salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(encoded_data)

        encrypted_data = salt + cipher.nonce + tag + ciphertext
        return encrypted_data

    def decrypt(self, encrypted_data):
        temp_file = "encryptedfile.bin"
        file_out = open(temp_file, "wb")
        file_out.write(encrypted_data)
        file_out.close()
        file_in = open(temp_file, "rb")
        salt, nonce, tag, ciphertext = [file_in.read(x) for x in (32, 16, 16, -1)]
        key = hashlib.scrypt(self.password, salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
        cipher = AES.new(key, AES.MODE_GCM, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        file_in.close()
        #os.remove(temp_file)
        return data.decode()
