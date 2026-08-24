from pwdlib import PasswordHash

class HashUtil:
    @staticmethod
    def hash_password(password:str):
        hasher=PasswordHash.recommended()
        return hasher.hash(password)

    @staticmethod
    def verify_password(password:str,hashed_password:str):
        hasher=PasswordHash.recommended()
        return hasher.verify(password,hashed_password)