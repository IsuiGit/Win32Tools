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
        serviceScanResponse = {}
        service = psutil.win_service_get(name)
        pid = service.pid()
        process_ = psutil.Process(pid)
        info_ = process_.as_dict()
        serviceScanResponse["username"] = "".join(["\t\t\t", info_["username"]])
        serviceScanResponse["cwd"] = "".join(["\t\t\t", info_["cwd"]])
        serviceScanResponse["pid"] = "".join(["\t\t\t", str(info_["pid"])])
        maps = []
        for memory_map in info_["memory_maps"]:
            if os.path.split(memory_map[0])[1].endswith('.dll') or os.path.split(memory_map[0])[1].endswith('.exe'):
                maps.append(memory_map[0])
        serviceScanResponse["memory_maps"] = "".join(["\t\t\t", "\n".join(maps)])
        return "\n".join([k+":"+v for k,v in serviceScanResponse.items()])
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
