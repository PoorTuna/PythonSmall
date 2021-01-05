import subprocess

# This is the main process which will run both of the processes

if __name__ == "__main__":
    proc_loc = subprocess.Popen(["python", "pass_loc.py", "V:/PythonWifi/"], stdout=subprocess.PIPE)
    end_of_pipe = proc_loc.stdout
    proc_print = subprocess.Popen(["python", "pass_print.py"], stdin= end_of_pipe ,stdout=subprocess.PIPE)
