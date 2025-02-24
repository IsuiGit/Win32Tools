from ctypes import CDLL, c_char_p, c_void_p, c_bool, c_int
import json
import sys

INPUTS = sys.argv

def loadJSON(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def bytesTranslation(obj):
    if isinstance(obj, str):
        return bytes(obj, "utf-8")
    else:
        return obj

def restypeCast(type):
    if type == "char*":
        return c_char_p
    elif type == "void*":
        return c_void_p
    elif type == "_Bool":
        return c_bool
    else:
        return c_int

def dllFuncTest(path=INPUTS[1], case=INPUTS[2]):
    try:
        dllFuncResponse = []
        dllTestCase = loadJSON(case)
        dll = CDLL(path)
        for case, args in dllTestCase.items():
            try:
                for i in range(args["iters"]):
                    func = getattr(dll, case)
                    func.restype = restypeCast(args["restype"])
                    if args["args"]:
                        c_args = []
                        for arg in args["args"]:
                            c_args.append(bytesTranslation(arg))
                        response = func(*c_args)
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
    if isinstance(dllFuncTestStdOut, bytes):
        sys.stdout.buffer.write(dllFuncTestStdOut)
    else:
        sys.stdout.buffer.write(dllFuncTestStdOut.encode())
