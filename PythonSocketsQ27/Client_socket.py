import socket
from PIL import Image
import base64

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 27010))

    choice = raw_input("Enter 1-4 [Screenshot,LaunchFile,ShowFolder/DeleteFiles,CopyFiles]")
    if choice == "1":
        client_socket.send('screen')

    elif choice == "2":
        client_socket.send('startf')

        file_path = raw_input('Please enter the directory of the file.')
        file_name = raw_input('What process would you like to launch from the directory?')
        file_path_len = len(file_path)
        file_name_len = len(file_name)

        client_socket.send(str(file_path_len))

        client_socket.send(str(file_name_len))

        client_socket.send(file_path)
        client_socket.send(file_name)

    elif choice == "3":
        client_socket.send('delete')
        folder_name = raw_input('Insert the desired folder you wish to look in')
        folder_name_len = len(folder_name)

        client_socket.send(str(folder_name_len))
        client_socket.send(folder_name)

        folder_item_count = client_socket.recv(6)
        for folder_file in range(0, int(folder_item_count), 1):
            folder_list_len = client_socket.recv(6)
            folder_file_name = client_socket.recv(int(folder_list_len))
            print folder_file_name

        message = '.'
        while message != '':
            message = raw_input('Enter the file you wish to delete!')
            client_socket.send(str(len(message)))
            client_socket.send(message)

    elif choice == "4":
        client_socket.send('copyfi')
        copy_path = raw_input('Enter the destination folder for the file you would like to copy')
        destination_path = raw_input('Enter the destination folder for the file you copied [Client Location]')

        copy_path_len = str(len(copy_path))

        client_socket.send(copy_path_len)
        client_socket.send(copy_path)

        indexlmao = 0
        folder_item_count = client_socket.recv(6)
        for folder_file in range(0, int(folder_item_count), 1):
            folder_list_len = client_socket.recv(6)
            folder_file_name = client_socket.recv(int(folder_list_len))
            print folder_file_name
            indexlmao = folder_file


        file_to_copy = raw_input('What file would you like to copy from the list?')
        file_to_copy_len = len(file_to_copy)

        client_socket.send(str(file_to_copy_len))
        client_socket.send(file_to_copy)

        img_msg = '.'
        img_data = ''
        while img_msg != '':
            img_msg = client_socket.recv(1024)
            img_data += img_msg

        img_data = base64.b64decode(img_data)

        with open('image.png', 'wb') as filefd:
            filefd.write(img_data)

        img = Image.open('image.png')
        img.show()

    else:
        print 'Invalid Choice Number!'

    client_socket.close()

except ValueError:
    print 'Error: The Server IS NOT Online! / The Server Forcibly Closed The Connection!'
