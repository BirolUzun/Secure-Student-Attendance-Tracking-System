from des import DesKey

DES_KEY = DesKey(b'98412347')


def encrypt_des(message):
    return DES_KEY.encrypt(message.encode(), padding=True)


def decrypt_des(encrypted_message):
    return DES_KEY.decrypt(encrypted_message, padding=True).decode()