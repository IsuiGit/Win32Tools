import sys
import importlib

INPUTS = sys.argv

def dllScan(path=INPUTS[1]):
    try:
        importlib.import_module('pefile')
    except ImportError:
        import pip
        pip.main(['install', 'pefile'])
    finally:
        globals()['pefile'] = importlib.import_module('pefile')
    try:
        dllScanResponse = ['\nDLL ENTRY_EXPORT LIST\n']
        pe = pefile.PE(path)
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            for export_ in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                dllScanResponse.append("\t\t\t".join([hex(pe.OPTIONAL_HEADER.ImageBase + export_.address), export_.name.decode(), str(export_.ordinal)]))
        return "\n".join(dllScanResponse)
    except Exception as e:
        return repr(e)

if __name__=='__main__':
    dllScanStdOut = dllScan()
    if isinstance(dllScanStdOut, bytes):
        sys.stdout.buffer.write(dllScanStdOut)
    else:
        sys.stdout.buffer.write(dllScanStdOut.encode())
