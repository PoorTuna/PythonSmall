import sys
import time

net_dir = ""
net_list = []

key_val_list = []


def find_root(par):
    if type(par) == type(list()):
        list_string = ""
        par.split("/")
        if "." in par[-1]:
            par.pop(-1)
        for item in par:
            list_string += item + "/"
        return list_string
    else:
        return "-1"


if __name__ == "__main__":
    data = sys.stdin.read()
    # Splitting between file_dir and network list
    data = data.split("|")
    file_path = data[0]
    network_list = data[1]
    network_list = network_list.split(".xml")

    index = 0
    # Adding back the .xml extension to xml files
    for network in network_list:
        network_list[index] = network + ".xml"
        index += 1

    # Extract name and password from xml files:
    for network in network_list:
        if network != ".xml":
            with open(file_path + network, "r") as filefd:
                net_name = "ERR"
                net_pass = "ERR"

                file_data = filefd.readlines()
                for line in file_data:
                    line = line.strip('\t')
                    if "<name>" in line:
                        net_name = line
                    if "<keyMaterial>" in line:
                        net_pass = line
                key_val_list.append([net_name, net_pass])

    # Remove garbage from the key_val list:
    keyval_index = 0
    for item in key_val_list:
        namepass_index = 0
        for namepass in item:
            index = 0
            # Get rid of garbage to the left
            for char in namepass:
                if char == ">":
                    break
                else:
                    index += 1
            namepass = namepass[index + 1:]

            # Get rid of garbage to the right
            index = 0
            for char in namepass:
                if char == "<":
                    break
                else:
                    index += 1
            namepass = namepass[:index]
            key_val_list[keyval_index][namepass_index] = namepass
            namepass_index += 1

        keyval_index += 1

    # Finally write name and passwords to a txt file:
    with open("networks.txt", "w") as filefd:
        filefd.write("KEY : VALUE \r\n")
        for item in key_val_list:
            filefd.write(item[0] + ":" + item[1] + "\r\n")
        key_val_list = "|".join(map(str, key_val_list))

    # Open the file and save a screenshot to the root dir:
    # img = Image.open("networks.txt")
    # img.save('saved_image', 'jpeg')
