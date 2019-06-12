from envmgr.models import Encryption

class Plain(Encryption):

    def encrypt(self, data):
        return data
    
    def decrypt(self, data):
        return data
