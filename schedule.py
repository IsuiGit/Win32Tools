import subprocess

def runProcess(tool, path=None, case=None):
    try:
        if not path or not case:
            return -1, "Error at parameters: no parameters sended"
        p = subprocess.Popen(["python", tool, path, case], stdout=subprocess.PIPE)
        response = p.communicate()[0].decode()
        return response
    except Exception as e:
        return repr(e)
