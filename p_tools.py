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
        service = psutil.win_service_get(name)
        return f"{service.as_dict()}"
    except psutil.NoSuchProcess:
        return f"No service named {INPUTS[1]}"

if __name__=='__main__':
    serviceFuncTestStdOut = serviceFuncTest()
    sys.stdout.buffer.write(serviceFuncTestStdOut.encode())
