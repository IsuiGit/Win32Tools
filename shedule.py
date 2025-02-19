import subprocess

def runProcess(path, case):
    if not path or not case:
        return -1, "Error at parameters: no parameters sended"
    p = subprocess.Popen(["python", "c_tools.py", path, case], stdout=subprocess.PIPE)
    response = p.communicate()[0].decode()
    return response
