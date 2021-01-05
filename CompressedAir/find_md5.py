import hashlib
import os

hash_code = "5e2a0c62c40b2cb4879b0081ec6db149"
for item in os.listdir():
    if ".jpg" in item:
        with open(item, "rb") as fd:
            if hash_code == hashlib.md5(fd.read()).hexdigest():
                print(item, " is the correct file!")
            else:
                print(item, " is the wrong file!")