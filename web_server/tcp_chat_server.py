import socket
import select

HEADER_LENGTH = 10
HOST = "127.0.0.1"
PORT = 12345

#create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

#listen to any connections
server_socket.listen()

socket_list = [server_socket]

clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        #TO-DO may need to strip message length to check the condition
        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8"))
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return client_message
    

while socket_list:
    '''select module is a direct interface to the underlying operating system implementation. It monitors 
    sockets, open files, and pipes (anything with a fileno() method that returns a valid file descriptor) 
    until they become readable or writable, or a communication error occurs.'''
    read_sockets, writable_sockets, error_sockets = select.select(socket_list, [], socket_list)
    
    for notified_socket in read_sockets:
        if notified_socket is server_socket:
            # New client is connecting
            client, client_addr = notified_socket.accept()
            print(f"New client {client_addr} got connnected")
            user = receive_message(client)
            if not user:
                continue
            socket_list.append(client)
            clients[client] = user
            print(f"Accepted new client from {client_addr[0]}:{client_addr[1]} of username: {user['data'].decode('utf-8')}")
        else:
            client_message = receive_message(notified_socket)
            if not client_message:
                # A client connection is closed
                print(f"Connection closed from {clients[notified_socket]['data'].decode('utf-8')}")
                socket_list.remove(notified_socket) 
                del clients[notified_socket]
                continue
            
            # A client is sending data
            user = clients[notified_socket]
            print(f"Received message from, {user['data'].decode('utf-8')}: {client_message['data'].decode('utf-8')}")
            
            # Send the received message to other clients
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + client_message['header'] + client_message['data'])

    for notified_socket in error_sockets:
        # Recieved an exception from socket
        socket_list.remove(notified_socket)
        del clients[notified_socket]
