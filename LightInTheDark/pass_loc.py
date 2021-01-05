import sys
import subprocess
import os
import time

# Process which locates all wifi passwords and saves them to location in the parameters. Deletes public wifi networks
del_count = 0
exp_dir = ""

def find_root(path):
    # This process finds the folder root for a full path

    list_string = ""
    path = path.split("/")
    if "." in path[-1]:
        path.pop(-1)
    for item in path:
        list_string += item + "/"
    return list_string


def del_open(file_path):
    # This process returns true if a network is public

    with open(file_path, "r") as filefd:
        data = filefd.readlines()
        for line in data:
            if "<authentication>open</authentication>" in line:
                return True
    return False


if __name__ == "__main__":
    pass_loc = subprocess.Popen(["netsh", "wlan", "show", "profile"], stdout=subprocess.PIPE)
    stdout, stderror = pass_loc.communicate()

    if len(stdout) > 0:
        if len(sys.argv) > 1:
            # check if theres a slash in the end of the path
            if sys.argv[1][-1] not in "\/":
                sys.argv[1] += "/"

            exp_dir = sys.argv[1]
            pass_loc_export = subprocess.Popen(["netsh", "wlan", "export", "profile", "folder=" + exp_dir, "key=clear"],
                                               stdout=subprocess.PIPE)

        else:
            print "error no parameters found! Using default folder!"

            exp_dir = "C:/WifiPass/"
            if not os.path.exists(exp_dir):
                os.mkdir(exp_dir)

            pass_loc_export = subprocess.Popen(["netsh", "wlan", "export", "profile", "folder=" + exp_dir, "key=clear"],
                                               stdout=subprocess.PIPE)

        # Delete public wifi networks :
        time.sleep(0.5)
        wifi_networks = os.listdir(exp_dir)
        if len(wifi_networks) > 0:
            for network in wifi_networks:
                if del_open(exp_dir + network):
                    del_count += 1
                    os.remove(exp_dir + network)
                    wifi_networks.remove(network)
            #print "wifis deleted:" + str(del_count)
        else:
            print "error! no wifi networks found!"

        # Write to the standard output:
        sys.stdout.write(str(exp_dir) + "|")
        for network in wifi_networks:
            sys.stdout.write(network)

        time.sleep(0.5)