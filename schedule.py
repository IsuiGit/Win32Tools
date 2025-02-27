import subprocess

def runProcess(tool, path=bytes(), case=bytes()):
    try:
        p = subprocess.Popen(['py', tool, path, case], stdout=subprocess.PIPE, shell=True)
        response = p.communicate()[0].decode()
        return f"\n### Solved with {tool} ###\n{response}"
    except Exception as e:
        return f"Exception at {tool} on path {path}: {repr(e)}"
