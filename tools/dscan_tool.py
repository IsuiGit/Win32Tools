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
        dllScanResponse = []
        pe = pefile.PE(path)
        if hasattr(pe, 'OPTIONAL_HEADER'):
            dllScanResponse.append('\nENTRY_POINT ADDRESS\n')
            dllScanResponse.append(hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            dllScanResponse.append('\nENTRY_EXPORT LIST\n')
            for export_ in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                try:
                    dllScanResponse.append("\t\t\t".join([hex(pe.OPTIONAL_HEADER.ImageBase + export_.address), export_.name.decode(), str(export_.ordinal)]))
                except:
                    pass
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            dllScanResponse.append('\nENTRY_IMPORT LIST\n')
            for import_ in pe.DIRECTORY_ENTRY_IMPORT:
                for im in import_.imports:
                    try:
                        dllScanResponse.append("\t\t\t".join([import_.dll.decode(), hex(im.address), im.name.decode()]))
                    except:
                        pass
        if not dllScanResponse:
            return "No IMAGE_DIRECTORY found"
        return "\n".join(dllScanResponse)
    except Exception as e:
        return repr(e)

if __name__=='__main__':
    dllScanStdOut = dllScan()
    if isinstance(dllScanStdOut, bytes):
        sys.stdout.buffer.write(dllScanStdOut)
    else:
        sys.stdout.buffer.write(dllScanStdOut.encode())
