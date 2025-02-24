from ctypes import CDLL
import json
import sys

INPUTS = sys.argv

def dllScan(path=INPUTS[1]):
    try:
        cdll_ = CDLL(path)
        return f"CDLL: {cdll_.__dict__}\n"
    except Exception as e:
        return repr(e)

if __name__=='__main__':
    dllScanStdOut = dllScan()
    if isinstance(dllScanStdOut, bytes):
        sys.stdout.buffer.write(dllScanStdOut)
    else:
        sys.stdout.buffer.write(dllScanStdOut.encode())
