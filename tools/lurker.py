import sys
import ctypes
import ctypes.wintypes
import os
import importlib

INPUTS = sys.argv

PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x04

kernel32 = ctypes.windll.kernel32

def createConnection(pid):
    if not isinstance(pid, int):
        try:
            pid = int(pid)
        except Exception as e:
            return False
    handler = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not handler:
        return False
    else:
        return handler

# Safe connection to process, with safe shutdown after connection
def lurkerInjection(path=INPUTS[1], pid=INPUTS[2]):
    try:
        dllLen = len(path)
        # Get target process
        handler = createConnection(pid)
        if not handler:
            return f"\nLurker can't open process at {pid}\n"
        # Allocate memory for the DLL path in the target process
        addr = kernel32.VirtualAllocEx(handler, None, dllLen, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)
        # Write the DLL path to the allocated memory
        kernel32.WriteProcessMemory(handler, addr, path, dllLen, None)
        # Get the address of LoadLibraryA
        kernel32Handler = kernel32.GetModuleHandleA(b'kernel32.dll')
        loadLibraryHandler = kernel32.GetProcAddress(kernel32Handler, b'LoadLibraryA')
        # Create a remote thread that calls LoadLibraryA with the DLL path
        threadId = ctypes.wintypes.DWORD()
        threadHandler = kernel32.CreateRemoteThread(handler, None, 0, loadLibraryHandler, addr, 0, ctypes.byref(threadId))
        # Wait for the thread to finish
        kernel32.WaitForSingleObject(threadHandler, 0xFFFFFFFF)
        # Clean up
        kernel32.VirtualFreeEx(handler, addr, 0, 0x8000)
        kernel32.CloseHandle(threadHandler)
        kernel32.CloseHandle(handler)
        return f"Lurker injection successfully at {pid}"
    except Exception as e:
        return f"\nLurker exit with exception {pid} with err: {e}\n"

if __name__ == "__main__":
    lurkerInjectionStdOut = lurkerInjection()
    if isinstance(lurkerInjectionStdOut, bytes):
        sys.stdout.buffer.write(lurkerInjectionStdOut)
    else:
        sys.stdout.buffer.write(lurkerInjectionStdOut.encode())
