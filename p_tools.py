import importlib
import json
import sys

INPUTS = sys.argv

def loadJSON(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def serviceFuncTest(name=INPUTS[1], case=INPUTS[2]):
    try:
        importlib.import_module('psutil')
    except ImportError:
        import pip
        pip.main(['install', 'psutil'])
    finally:
        globals()['psutil'] = importlib.import_module('psutil')
    try:
        pid = psutil.win_service_get(name).pid()
        exe = psutil.Process(pid).exe()
        if exe and 'svchost' not in exe:
            #from subprocess import Popen, PIPE
            #p = Popen([exe], stdout=PIPE)
            #response = p.communicate()[0]
            return exe
        else:
            return f"{INPUTS[1]}: the path to the executable file for the selected service was not found or it is internal to the system (svchost.exe) "
    except psutil.NoSuchProcess:
        return f"No service named {INPUTS[1]}"

if __name__=='__main__':
    serviceFuncTestStdOut = serviceFuncTest()
    if isinstance(serviceFuncTestStdOut, bytes):
        sys.stdout.buffer.write(serviceFuncTestStdOut)
    else:
        sys.stdout.buffer.write(serviceFuncTestStdOut.encode())
