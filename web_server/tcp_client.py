import socket
import pickle

#create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connecting to server
s.connect((socket.gethostname(), 5688))

HEADER_LENGTH = 10
full_msg = b''
new_msg = True
while True:
    msg = s.recv(16)
    if new_msg:
        print('length of the new message is', msg[:HEADER_LENGTH])
        msg_len = int(msg[:HEADER_LENGTH])
        new_msg = False
    full_msg += msg

    if len(full_msg) - HEADER_LENGTH == msg_len:
        print('full message received:', full_msg[HEADER_LENGTH:])
        print(pickle.loads(full_msg[HEADER_LENGTH:]))
        new_msg = True
        full_msg = b''

#s.send(bytes('Hello from client', 'utf-8'))

#new_msg = s.recv(1024)
#print(new_msg.decode("utf-8"))
print(full_msg)
#s.close()