import socket
import select
import errno
import sys
import threading

HEADER_LENGTH = 10
HOST = "127.0.0.1"
PORT = 12345
my_username = input("Username: ")

#create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#set recv data method to non-blocking in client socket
#change this and check how code works
client_socket.setblocking(0)

#server is ecpecting user info first
username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

def get_message_input():
    while True:
        # message we want to send
        my_message = input(f"{username} > ")
        if my_message:
            message = my_message.encode("utf-8")
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + message)

message_thread = threading.Thread(target=get_message_input, daemon=True)
message_thread.start()

while True:
    """
        # This code using select and sys.stdin won't work on windows
        input = select.select([sys.stdin], [], [])[0]
        if input:
            my_message = sys.stdin.readline().rstrip()
    """
    # receive message from server
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed by server")
                sys.exit()
            
            username_length = int(username_header.decode("utf-8"))
            recv_username = client_socket.recv(username_length)

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf=8"))
            recv_message = client_socket.recv(message_length)
            print(f'{recv_username} > {recv_message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data, error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: ', e)
            sys.exit()

        #We just did not receive anything
        continue

    except Exception as e:
        #Any other exception - something happened, exit
        print('Reading error: ', e)
        sys.exit()
