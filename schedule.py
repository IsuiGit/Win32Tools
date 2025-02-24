import subprocess

def runProcess(tool, path=bytes(), case=bytes()):
    try:
        p = subprocess.Popen(["python", tool, path, case], stdout=subprocess.PIPE)
        response = p.communicate()[0].decode()
        return response
    except Exception as e:
        return f"Exception at {tool} on path {path}: {repr(e)}"
