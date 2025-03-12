import random
import hashlib
import base64

def genVerifier():
    # Generates a random string that follows PKCE requirements (specific charset, urlsafe base64, without '=')
    charset ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~_-.' 
    codeVerifier = ''.join(random.choices(charset, k=128))

    print(f'The code verfier: {codeVerifier}')
    return codeVerifier

def genChallenge(codeVerifier: str):
    hash = hashlib.sha256(codeVerifier.encode())
    hash = hash.digest()
    codeChallenge = base64.urlsafe_b64encode(hash).decode().strip('=')

    print(f'The code verfier: {codeChallenge}')
    return codeChallenge