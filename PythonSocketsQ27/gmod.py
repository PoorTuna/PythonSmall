import socket

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect(("109.65.84.220",27016))


client_socket.send("sex")