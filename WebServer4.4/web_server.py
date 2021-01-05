import socket
import select
import os

SERVER_PORT = 80
CONNECTION = True
ROOT_FOLDER = r"C:/Users/Oren/Desktop/webroot"
STATUS_ANSWER = "200 OK"

web_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
web_server.bind(('0.0.0.0', SERVER_PORT))

web_server.listen(10)

open_client_socket = []

while CONNECTION:
    rlist, wlist, xlist = select.select([web_server] + open_client_socket, open_client_socket, [])
    for socket in rlist:
        if socket is web_server:
            new_client, address = web_server.accept()
            open_client_socket.append(new_client)

        else:
            data = socket.recv(4096)
            if data == "":  # Makes sure that the request exists.
                open_client_socket.remove(socket)
                socket.close()

            # FIRST LINE SECTION :

            else:
                forbidden_file = False  # if stauts code is 304 then this turns to true in order to prevent user from accessing the file.

                first_line = data.split(" ")
                if len(first_line) >= 2:  # Makes sure if the request is valid by its length.
                    if r"\r\n" not in first_line[2]:
                        if socket not in open_client_socket:
                            open_client_socket.remove(socket)
                            socket.close()

                    if first_line[0] != "GET" or ("HTTP/1.1\r\n" in first_line[1]
                                                  or "HTTP/1.1\r\n" not in first_line[
                                                      2]):  # Checks if the request is invalid

                        if socket not in open_client_socket:
                            STATUS_ANSWER = "500 Internal Service Error"
                    elif "HTTP/1.1\r\n" in first_line[2]:
                        first_line[2] = "HTTP/1.1"

                        while len(first_line) != 3 or len(first_line) == 0:
                            first_line.pop(-1)

                    # REST OF REQUEST :
                    # file content :
                    content = ""
                    content_type = "text/html charset=utf-8"
                    requested_path = first_line[1]
                    requested_file = first_line[1].split("/")
                    requested_file = requested_file[-1]
                    file_path = str(ROOT_FOLDER + first_line[1])
                    if ".html" in requested_path:
                        content_type = "text/html charset=utf-8"

                    if ".png" in requested_path or ".jpg" in requested_path or ".jpeg" in requested_path or ".ico":
                        content_type = "image/png"

                    if ".js" in requested_path:
                        content_type = "text/javascript"

                    if ".css" in requested_path:
                        content_type = "text/css"
                        forbidden_file = True

                    # URL handling :
                    if requested_path == "/" or first_line[1] == "\\"[0:1:1]:
                        requested_file = "index.html"

                        if os.path.exists(ROOT_FOLDER + requested_path):
                            with open((ROOT_FOLDER + requested_path + requested_file), "rb") as file_fd:
                                content = file_fd.read()
                    else:
                        if os.path.exists(file_path) or "page1.html" in requested_path or "calculate-next" in requested_path:
                            requested_file = first_line[1].split("/")
                            requested_file = requested_file[-1]

                            if "calculate-next" not in requested_path:
                                if "page1.html" in requested_path:
                                    STATUS_ANSWER = "302 Temporarily Moved"
                                    requested_path = requested_path[requested_path.find("page1.html")::1].replace("1","2")
                                    file_path = ROOT_FOLDER + "/" + requested_path

                                if not forbidden_file:
                                    with open(file_path, "rb") as file_fd:
                                        content = file_fd.read()
                                        STATUS_ANSWER = "200 OK"
                            elif "calculate-next" in requested_path:
                                STATUS_ANSWER = "200 OK"
                                content = requested_file.split("=")
                                content = str(int(content[-1]) + 1)

                            else:
                                STATUS_ANSWER = "302 Temporarily Moved"
                                content = "<html><body style=background-color:grey;color:yellow;font-size:5cm><span>File cant be accessed! Err 302 Temporarily Moved</span></body></html>"

                        else:
                            content = "<html><body style=background-color:grey;color:yellow;font-size:5cm><span>File not found! Err 404</span></body></html>"
                            STATUS_ANSWER = "404 Not Found"

                    # Finding Host Header + Content Length Header
                    message_headers_Host = ""
                    message_lineOne = first_line[2] + " " + STATUS_ANSWER + r"\n\r"
                    headers = data.split("\r\n")
                    content_length = len(content)
                    for header in headers:
                        if "Host:" in header:
                            message_headers_Host = header
                    # After Host has been found
                    RESPONSE = message_lineOne + message_headers_Host + "Content-Type: " + content_type + "\r\n" + "Content-Length:" + str(
                            content_length) + "\r\n" + "\r\n" + str(content)
                    socket.send(RESPONSE)

web_server.close()
