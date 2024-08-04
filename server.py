import socket
from cryptography.fernet import Fernet

s = socket.socket(socket.AF_INET,
                socket.SOCK_STREAM)

s.connect(('127.0.0.1', 5000))

msg = s.recv(1024)

while msg:
    print('Received:' + msg.decode())
    if msg.decode()[0:3]=='car':
        with open('filekey.key', 'rb') as filekey:
                        key = filekey.read()
                     
                    # using the generated key
        fernet = Fernet(key)
        with open('PIC_encrypted.png', 'rb') as enc_file:
            encrypted = enc_file.read()
         
        # decrypting the file
        decrypted = fernet.decrypt(encrypted)
         
        # opening the file in write mode and
        # writing the decrypted data
        with open('new_pic_recieved.png', 'wb') as dec_file:
            dec_file.write(decrypted)

    msg = s.recv(1024)

# disconnect the client
#s.close()
