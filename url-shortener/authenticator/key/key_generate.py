
from Crypto.PublicKey import RSA

keypair = RSA.generate(bits=1024)
with open('public_key.pem', 'wb') as f:
    f.write(keypair.publickey().exportKey(format='PEM'))

with open('private_key.pem', 'wb') as f:
    f.write(keypair.exportKey(format='PEM'))