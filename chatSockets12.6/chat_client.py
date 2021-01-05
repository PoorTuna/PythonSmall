import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 27016
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

connection = True

while connection:

    data = raw_input('Please share with us your info :) [0 to quit]')
    data_length = len(data)

    client_socket.send(str(data_length))

    client_socket.send(data)

    message_len = int(client_socket.recv(10))
    message = client_socket.recv(message_len)
    print 'The server replies with : ' + message
    if data == '0':
        connection = False
