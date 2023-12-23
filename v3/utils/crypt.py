import pickle


from cryptography.fernet import Fernet

cipher_suite = Fernet(Fernet.generate_key())


def encrypt_data(data):
    return cipher_suite.encrypt(pickle.dumps(data))


def decrypt_data(data):
    return pickle.loads(cipher_suite.decrypt(data))
