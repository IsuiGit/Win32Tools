from ctypes import CDLL
import json
import sys

INPUTS = sys.argv

def loadJSON(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def dllFuncTest(path=INPUTS[1], case=INPUTS[2]):
    try:
        dllFuncResponse = []
        dllTestCase = loadJSON(case)
        dll = CDLL(path)
        for case, args in dllTestCase.items():
            try:
                for i in range(args["iters"]):
                    func = getattr(dll, case)
                    if args["args"]:
                        response = func(*args["args"])
                    else:
                        response = func()
                    dllFuncResponse.append(f"{case}: {response}")
            except Exception as e:
                dllFuncResponse.append(f"{case}: {repr(e)}")
        return '\n'.join(dllFuncResponse)
    except Exception as e:
        return repr(e)

if __name__=='__main__':
    dllFuncTestStdOut = dllFuncTest()
    sys.stdout.buffer.write(dllFuncTestStdOut.encode())
