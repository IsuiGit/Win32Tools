import importlib
import sys
import os

INPUTS = sys.argv

def serviceScan(name=INPUTS[1]):
    try:
        importlib.import_module('psutil')
    except ImportError:
        import pip
        pip.main(['install', 'psutil'])
    finally:
        globals()['psutil'] = importlib.import_module('psutil')
    try:
        service = psutil.win_service_get(name)
        pid = service.pid()
        process_ = psutil.Process(pid)
        info_ = process_.as_dict()
        return '\n'.join([f"{k.upper()}:{v}" for k,v in info_.items() if v])
    except psutil.NoSuchProcess:
        return f"No service named {INPUTS[1]}"
    except psutil.AccessDenied:
        return f"Access denied {INPUTS[1]}, try running the program as administrator!"

if __name__=='__main__':
    serviceScanStdOut = serviceScan()
    if isinstance(serviceScanStdOut, bytes):
        sys.stdout.buffer.write(serviceScanStdOut)
    else:
        sys.stdout.buffer.write(serviceScanStdOut.encode())
