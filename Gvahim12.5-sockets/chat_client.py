import socket
import select
import msvcrt
from datetime import datetime

SERVER_PORT = 80
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', SERVER_PORT))

connection = True
server_messages = []
messages_to_send = []
name = raw_input('Please insert your name')


def message_to_send(write_list):
    for item in messages_to_send:
        client_sock, client_data = item
        if client_sock in write_list:
            client_sock.send(client_data)


while connection:
    rlist, wlist, xlist = select.select([client_socket], [client_socket], [])
    for messages in rlist:
        data = client_socket.recv(2000)
        if data != "":
            print data
    message = ''
    if msvcrt.kbhit():
        message = msvcrt.getch()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if message == 'quit':
        connection = False
    elif message != '':
        message = '[' + str(current_time) + '] ' + '[' + name + '] ' + str(message)
        messages_to_send.append((client_socket, message))

    message_to_send(wlist)
