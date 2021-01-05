
file_path = "C:/Users/Oren/Desktop/webroot/index.html"
with open(file_path , "rb") as file_fd:
    content = file_fd.read()
    print content