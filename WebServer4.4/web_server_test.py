import socket
import select
import os

SERVER_PORT = 80
WEB_ROOT_ADDRESS = "C:/Users/Oren/Desktop/webroot/"

web_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
web_server.bind(('0.0.0.0', SERVER_PORT))

web_server.listen(10)


connection = True
open_client_list = []

while connection:
    rlist,wlist,xlist = select.select([web_server] + open_client_list , open_client_list , [])

    for socket in rlist:
        if socket is web_server:
            socket,socket_ip = web_server.accept()
            open_client_list.append(socket)

        else:
            answer_plus_phrase = "200 OK"
            is_forbidden = False # Variable to block certain files from user
            ok_check = False
            data = socket.recv(4096)

            if data != "":
                print data
                data = data.split("\r\n")
                if "HTTP/1.1" in data[0] and "GET" in data[0]:
                    first_line = data[0].split(" ")
                    URL = first_line[1]

                    # Headers
                    content_type = ""
                    content_len = 0
                    HOST = "127.0.0.1"

                    # Resources
                    content = ""

                    # Check if url exists :
                    if os.path.exists(WEB_ROOT_ADDRESS + URL) or "page1.html" in URL or "calculate-next" in URL:

                        # Content Type :
                        if ".jpg" in URL or ".jpeg" in URL or ".png" in URL:
                            content_type = "image/jpg"
                        if ".css" in URL:
                            is_forbidden = True
                        if ".html" in URL:
                            content_type = "text/html"
                        if ".mp3" in URL or ".wav" in URL:
                            content_type = "audio/x-wav"
                        if ".js" in URL:
                            content_type = "text/javascript; charset=UTF-8"
                        else:
                            content_type = "text/html charset=utf-8"
                        # Content :
                        if "/" == URL or "\\"[0:1:1] == URL:
                            URL = "/index.html"

                        elif "page1.html" in URL:
                            ok_check = True
                            URL = "/page2.html"
                            answer_plus_phrase = "302 Moved Temporarily"
                        elif "calculate-next" in URL:
                            print 1
                            parameters = URL.split("?")
                            num_value = parameters[1].split("=")
                            content = str(int(num_value[1]) + 1)
                            answer_plus_phrase = "200 OK"

                        if not is_forbidden and "calculate-next" not in URL:
                            file_path = WEB_ROOT_ADDRESS + URL
                            with open(file_path , "rb") as file_fd:
                                content = file_fd.read()
                                if not ok_check:
                                    answer_plus_phrase = "200 OK"
                        else:
                            content = "403 forbidden access!"
                            answer_plus_phrase = "403 Forbidden"


                    else:
                        content = "Err 404 page not found!"
                        answer_plus_phrase = "404 Not found"

                    # Response Message :
                    message_headers_Host = ""
                    first_line_response = first_line[2] + " " +answer_plus_phrase + "\r\n"
                    content_len = len(content)
                    for header in data:
                        if "Host:" in header:
                            message_headers_Host = header
                    RESPONSE = first_line_response + message_headers_Host + "\r\n"+ "Content-Type: " + content_type + "\r\n" + "Content-Length:" + str(
                            content_len) + "\r\n" + "\r\n" + str(content)
                    socket.send(RESPONSE)

