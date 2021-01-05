import socket
from PIL import ImageGrab
import sys
import subprocess
import os

import base64

if len(sys.argv) < 4:
    exit(ValueError)
# Server Def:
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 27010))
server_socket.listen(1)

client_socket, address = server_socket.accept()

ChoiceData = client_socket.recv(6)  # The length of the decision data [Constant]

if ChoiceData == 'screen':
    img = ImageGrab.grab()
    img.save(sys.argv[1] + sys.argv[2] + '.' + sys.argv[3], sys.argv[3])

elif ChoiceData == 'startf':
    path_len = client_socket.recv(6)
    file_len = client_socket.recv(6)

    path_name = client_socket.recv(int(path_len))
    exe_name = client_socket.recv(int(file_len))

    check = False
    try:
        dir_list = os.listdir(path_name)
        for item in dir_list:
            if exe_name in item:
                check = True
        if not check:
            client_socket.close()
            exit('Invalid File Name!')
    except WindowsError:
        client_socket.close()
        exit('Invalid File Path!')

    subprocess.call(path_name + r'\\' + exe_name, shell=True)

elif ChoiceData == 'delete':
    folder_path_len = client_socket.recv(6)
    folder_path = client_socket.recv(int(folder_path_len))
    try:
        list_dir = os.listdir(folder_path)
        client_socket.send(str(len(list_dir)))
        for item in list_dir:  # List dir item
            item_len = len(item)
            client_socket.send(str(item_len))
            client_socket.send(item)

    except WindowsError:
        client_socket.close()
        exit('Invalid Directory Name')

    message = "message"
    while message != '':
        message_len = client_socket.recv(6)
        message = client_socket.recv(int(message_len))

        check = False
        listdir = os.listdir(folder_path)
        for file_name in listdir:
            if message == file_name:
                os.remove(folder_path + '/' + message)

        if not check:
            client_socket.send('Invalid File Name!')

elif ChoiceData == 'copyfi':
    data_message = '.'

    data_path_len = client_socket.recv(6)
    data_path = client_socket.recv(int(data_path_len))
    try:
        list_dir = os.listdir(data_path)
        client_socket.send(str(len(list_dir)))
        for item in list_dir:  # List dir item
            item_len = len(item)
            client_socket.send(str(item_len))
            client_socket.send(item)

        data_to_copy_len = client_socket.recv(6)
        data_to_copy = client_socket.recv(int(data_to_copy_len))

        with open(data_path + data_to_copy, 'rb') as filefd:
            binary_data_string = filefd.read()
            base64Data = base64.b64encode(binary_data_string)
            base64Data_len = len(base64Data)
            base64Data_len_og = base64Data_len
            print 'File size : ' + str(base64Data_len)

        while base64Data_len >= 1024 or base64Data_len - 1024 > 0:
            client_socket.send(base64Data)
            base64Data_len -= 1024
            print 'Downloaded :' + str(base64Data_len_og - base64Data_len)

    except WindowsError:
        client_socket.close()
        exit('Invalid Directory Name')


else:
    exit('Invalid Input!')
server_socket.close()
