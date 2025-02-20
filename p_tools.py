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
        result = []
        serviceTestCase = loadJSON(case)
        service = psutil.win_service_get(name)
        pid = service.pid()
        process = psutil.Process(pid)
        dlls = {os.path.split(dll.path)[1]:dll.path for dll in process.memory_maps() if dll.path.endswith('.dll')}
        if not dlls:
            return f"No dlls found at service {INPUTS[1]}"
        for dllName in serviceTestCase.keys():
            if dllName in dlls.keys():
                result.append(f"Found {dlls[dllName]} at process {INPUTS[1]}")
        if not result:
            return f"The {list(serviceTestCase.keys())} DLL components were not found in the service"
        return '\n'.join(result)
    except psutil.NoSuchProcess:
        return f"No service named {INPUTS[1]}"
    except psutil.AccessDenied:
        return f"Access denied {INPUTS[1]}, try running the program as administrator!"

if __name__=='__main__':
    serviceFuncTestStdOut = serviceFuncTest()
    if isinstance(serviceFuncTestStdOut, bytes):
        sys.stdout.buffer.write(serviceFuncTestStdOut)
    else:
        sys.stdout.buffer.write(serviceFuncTestStdOut.encode())
