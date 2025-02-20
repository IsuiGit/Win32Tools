import importlib
import json
import sys
import os

INPUTS = sys.argv
EXCEPT_NAME = ['svchost.exe', 'python.exe']

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
        if not exe or os.path.split(exe)[1] in EXCEPT_NAME:
            return f"{INPUTS[1]}: the path to the executable file for the selected service was not found or it is internal to the system {EXCEPT_NAME}"
        else:
            serviceTestCase = loadJSON(case)
            try:
                comma = serviceTestCase["flags"]
            except KeyError:
                return f"Test case must include flag section with text params"
            from subprocess import Popen, PIPE
            try:
                p = Popen([exe, *comma], stdout=PIPE)
                response = p.communicate()[0]
                return response
            except Exception as e:
                return repr(e)
    except psutil.NoSuchProcess:
        return f"No service named {INPUTS[1]}"

if __name__=='__main__':
    serviceFuncTestStdOut = serviceFuncTest()
    if isinstance(serviceFuncTestStdOut, bytes):
        sys.stdout.buffer.write(serviceFuncTestStdOut)
    else:
        sys.stdout.buffer.write(serviceFuncTestStdOut.encode())
