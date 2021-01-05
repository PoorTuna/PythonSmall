import zipfile

ROOT_DIR = ""
ZIP_DIR = "wifi.zip"
FILE_DIR = ROOT_DIR + ZIP_DIR

zip_file = zipfile.ZipFile(FILE_DIR)

with open(ROOT_DIR + "com_pass.txt", "r") as fd:
    for line in fd.readlines():
        try:
            zip_file.extractall(pwd=line.strip().encode())
            print('SUCCESS : PASSWORD = ', line)
            break
        except RuntimeError:
            print("Password = ", line, " is wrong!")

# CORRECT PASSWORD = 1234qwer
