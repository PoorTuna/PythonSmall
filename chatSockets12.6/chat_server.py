import select
import socket

IP_RANGE = '0.0.0.0'
SERVER_PORT = 27129
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP_RANGE, SERVER_PORT))

open_client_sockets = []
server_socket.listen(10)

messages_to_send = []


def messages_to_send_func(wlist_fun):
    for client_message in messages_to_send:
        (client_socket_wlist, data) = client_message
        if client_socket_wlist in wlist_fun:

            client_socket_wlist.send(str(len(data)))
            client_socket_wlist.send(data)
            messages_to_send.remove(client_message)


while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
    for client in rlist:
        if client is server_socket:
            (client_socket, client_address) = server_socket.accept()
            open_client_sockets.append(client_socket)
        else:
            message_len =  client.recv(8)
            message = client.recv(int(message_len))
            if message == '0' or message == "":
                open_client_sockets.remove(client)
                print 'Connection terminated with  ' + str(client)

            if message != "":
                print message
                messages_to_send.append((client, "Hello " + message))

    messages_to_send_func(wlist)
