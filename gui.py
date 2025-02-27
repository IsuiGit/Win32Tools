from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import scrolledtext as st
from tkinter.messagebox import askyesno
import settings

class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Presets
        self.title("Win32 Tools")
        self.geometry("800x600")
        # Menu
        menubar = Menu(self)
        dllmenu = Menu(menubar, tearoff=0)
        dllmenu.add_command(label="Run .dll calls", command=self.runDllTests)
        servicemenu = Menu(menubar, tearoff=0)
        servicemenu.add_command(label="Run service calls --IN WORK")
        analysismenu = Menu(menubar, tearoff=0)
        analysismenu.add_command(label="Entry scan", command=self.dllScan)
        analysismenu.add_command(label="Service scan", command=self.serviceScan)
        lurkermenu = Menu(menubar, tearoff=0)
        lurkermenu.add_command(label="Inject (dangerous)", command=self.lurkerInject)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Clear", command=self.clearOutput)
        menubar.add_cascade(label=".dll", menu=dllmenu)
        menubar.add_cascade(label="Win32 services", menu=servicemenu)
        menubar.add_cascade(label="Analysis", menu=analysismenu)
        menubar.add_cascade(label="Lurker", menu=lurkermenu)
        menubar.add_cascade(label="Edit", menu=editmenu)
        # Textarea
        self.text = st.ScrolledText(wrap="word")
        self.text.pack(fill=BOTH, expand=1)
        # Config
        self.config(menu=menubar)

    def lurkerInject(self):
        result = askyesno(title="Unsafe function", message="Warning! This feature is experimental and unreliable (in particular, it can harm the operating system). Are you sure you want to use it?")
        if result:
            pid = None
            try:
                procID = simpledialog.askstring("Get process ID", "Enter the process ID\t\t\t")
                if procID != "":
                    if procID.isnumeric():
                        pid = procID
                    else:
                        self.text.insert(END, "pid can only contain numbers!")
                        self.text.insert(END, ''.join("-" for i in range(50))+'\n')
                        return False
                else:
                    self.text.insert(END, f"Process ID is: {procID}\n")
                    self.text.insert(END, ''.join("-" for i in range(50))+'\n')
                    return False
            except Exception as e:
                self.text.insert(END, f"{e}\n")
            from tools.thread_tool import runThread
            from schedule import runProcess
            if not pid:
                self.text.insert(END, "Process ID not specified\n")
                self.text.insert(END, ''.join("-" for i in range(50))+'\n')
            else:
                lurkerInjectionResponse = runThread(runProcess, args=[settings.LURKER_TOOL, settings.LURKER_INJECTION, pid])
                self.text.insert(END, f"{lurkerInjectionResponse}"+"\n")
                self.text.insert(END, ''.join("-" for i in range(50))+'\n')
        else:
            self.text.insert(END, "Operation canceled\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')

    def clearOutput(self):
        self.text.delete('1.0', END)

    def serviceScan(self):
        service_name = None
        try:
            serviceName = simpledialog.askstring("Get service name", "Enter the service name\t\t\t")
            if serviceName != "":
                service_name = serviceName
                self.text.insert(END, f"service name is: {serviceName}\n")
        except Exception as e:
            self.text.insert(END, f"{e}\n")
        from tools.thread_tool import runThread
        from schedule import runProcess
        if not service_name:
            self.text.insert(END, "Service name not specified\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')
        else:
            serviceScanResponse = runThread(runProcess, args=[settings.SERVICE_SCAN_TOOL, service_name])
            self.text.insert(END, f"{serviceScanResponse}"+"\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')

    def dllScan(self):
        dll_path = None
        try:
            filepath = filedialog.askopenfilename(title="Выбор файла", filetypes=[("Dynamic Link Library", "*.dll"), ("Executable files", "*.exe")])
            if filepath != "":
                dll_path = filepath
                self.text.insert(END, f"Module {filepath} loaded\n")
        except Exception as e:
            self.text.insert(END, f"{e}\n")
        from tools.thread_tool import runThread
        from schedule import runProcess
        if not dll_path:
            self.text.insert(END, "No modules imported\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')
        else:
            dllScanResponse = runThread(runProcess, args=[settings.MODULE_SCAN_TOOL, dll_path])
            self.text.insert(END, f"{dllScanResponse}"+"\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')

    def getTestCasePath(self):
        try:
            filepath = filedialog.askopenfilename(title="Выбор файла", filetypes=[("JSON file", "*.json")])
            if filepath != "":
                self.text.insert(END, f"Call template {filepath} loaded\n")
                return filepath
        except Exception as e:
            self.text.insert(END, f"{e}\n")

    def runDllTests(self):
        dll_path = None
        try:
            filepath = filedialog.askopenfilename(title="Выбор файла", filetypes=[("Dynamic Link Library", "*.dll")])
            if filepath != "":
                dll_path = filepath
                self.text.insert(END, f"Module {filepath} loaded\n")
        except Exception as e:
            self.text.insert(END, f"{e}\n")
        case_path = self.getTestCasePath()
        from tools.thread_tool import runThread
        from schedule import runProcess
        if not dll_path or not case_path:
            self.text.insert(END, "No modules or call templates imported\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')
        else:
            dllFuncTestResponse = runThread(runProcess, args=[settings.MODULE_TOOL, dll_path, case_path])
            self.text.insert(END, dllFuncTestResponse+'\n')
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')
