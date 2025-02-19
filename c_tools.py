from ctypes import CDLL
import json

def loadJSON(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def dllFuncTest(path, case):
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
            dllFuncResponse.append(repr(e))
    return dllFuncResponse
