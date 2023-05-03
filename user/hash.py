import hashlib

def hashing(password):
    h = hashlib.sha256()
    h.update(password.encode())

    return h.hexdigest()