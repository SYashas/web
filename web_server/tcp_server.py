import socket
import time
import pickle

#create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind ip_address and port_number to socket
#s.bind((socket.gethostname(), 5688))
s.bind(("0.0.0.0", 5688))

#max connections that socket can listen at a time
s.listen(5)

HEADER_LENGTH = 10

#accept client connection
while True:
    client, address = s.accept()
    print(f"Connection established from {address} client!")
    print(f"Client info: {client}")
    msg = 'Welcome to the Server!'
    msg = pickle.dumps(msg)
    msg = bytes(f'{len(msg):<{HEADER_LENGTH}}', "utf-8") + msg
    #client.send(bytes(msg, "utf-8"))
    client.send(msg)
    time.sleep(3)
    """#Receiving data from client
    recv_msg = client.recv(1024)
    print(recv_msg.decode("utf-8"))
    client.send(recv_msg)"""

    msg = {"name":"yashas", "message": "hello world"}
    msg = pickle.dumps(msg)
    msg = bytes(f'{len(msg):<{HEADER_LENGTH}}', "utf-8") + msg
    client.send(msg)
    '''while True:
        time.sleep(3)
        msg = f'the current timr is {time.time()}'
        msg = f'{len(msg):<{HEADER_LENGTH}}' + msg
        client.send(bytes(msg, "utf-8"))'''
    """while True:
        recv_msg = client.recv(1024)
        recv_msg = recv_msg.decode("utf-8")
        if not recv_msg:
            s.close()
        print(recv_msg)
        client.send(bytes(recv_msg, "utf-8"))"""
s.close()
