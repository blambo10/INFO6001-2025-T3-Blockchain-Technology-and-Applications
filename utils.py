import hashlib

def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()