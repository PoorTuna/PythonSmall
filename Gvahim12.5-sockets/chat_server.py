import socket
import select

SERVER_PORT = 27091
open_client_sockets = []
message_to_send = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', SERVER_PORT))
server_socket.listen(100)


def messages_to_send(write_list, client_list):
    for message in message_to_send:
        client_socket, clnt_data = message
        for client in client_list:
            if client is not client_socket and client in write_list:
                client.send(clnt_data)
                message_to_send.remove(message)


while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
    for client_read in rlist:
        if client_read is server_socket:
            client_sock, client_address = server_socket.accept()
            open_client_sockets.append(client_sock)

        else:
            print ' '
            data = client_read.recv(2000)
            print 'message received!'
            message_to_send.append((client_read, data))

    messages_to_send(wlist, open_client_sockets)
