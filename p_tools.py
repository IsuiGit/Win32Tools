import importlib
import json
import sys
import os

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
        service = psutil.win_service_get(name)
        return f"binpath: {service.binpath()}"
    except psutil.NoSuchProcess:
        return f"No service named {INPUTS[1]}"
    except psutil.AccessDenied:
        return f"Access denied {INPUTS[1]}"

if __name__=='__main__':
    serviceFuncTestStdOut = serviceFuncTest()
    if isinstance(serviceFuncTestStdOut, bytes):
        sys.stdout.buffer.write(serviceFuncTestStdOut)
    else:
        sys.stdout.buffer.write(serviceFuncTestStdOut.encode())
