from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import scrolledtext as st

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
        menubar.add_cascade(label=".dll", menu=dllmenu)
        menubar.add_cascade(label="Win32 services", menu=servicemenu)
        menubar.add_cascade(label="Analysis", menu=analysismenu)
        # Textarea
        self.text = st.ScrolledText(wrap="word")
        self.text.pack(fill=BOTH, expand=1)
        self.text.bind("<Key>", lambda e: "break")
        # Config
        self.config(menu=menubar)

    def serviceScan(self):
        service_name = None
        try:
            serviceName = simpledialog.askstring("Get service name", "Enter the service name for the test\t\t\t")
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
            serviceScanResponse = runThread(runProcess, args=["./tools/sscan_tool.py", service_name])
            self.text.insert(END, f"{serviceScanResponse}"+"\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')

    def dllScan(self):
        dll_path = None
        try:
            filepath = filedialog.askopenfilename(title="Выбор файла", filetypes=[("Dynamic Link Library", "*.dll"), ("Executable files", "*.exe")])
            if filepath != "":
                dll_path = filepath
                self.text.insert(END, f"dll lib {filepath} loaded\n")
        except Exception as e:
            self.text.insert(END, f"{e}\n")
        from tools.thread_tool import runThread
        from schedule import runProcess
        if not dll_path:
            self.text.insert(END, "No dll imported\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')
        else:
            dllScanResponse = runThread(runProcess, args=["./tools/dscan_tool.py", dll_path])
            self.text.insert(END, f"{dllScanResponse}"+"\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')

    def getTestCasePath(self):
        try:
            filepath = filedialog.askopenfilename(title="Выбор файла", filetypes=[("JSON file", "*.json")])
            if filepath != "":
                self.text.insert(END, f"test case {filepath} loaded\n")
                return filepath
        except Exception as e:
            self.text.insert(END, f"{e}\n")

    def runDllTests(self):
        dll_path = None
        try:
            filepath = filedialog.askopenfilename(title="Выбор файла", filetypes=[("Dynamic Link Library", "*.dll")])
            if filepath != "":
                dll_path = filepath
                self.text.insert(END, f"dll lib {filepath} loaded\n")
        except Exception as e:
            self.text.insert(END, f"{e}\n")
        case_path = self.getTestCasePath()
        from tools.thread_tool import runThread
        from schedule import runProcess
        if not dll_path or not case_path:
            self.text.insert(END, "No dll modules or test case file imported\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')
        else:
            dllFuncTestResponse = runThread(runProcess, args=["./tools/dll_tool.py", dll_path, case_path])
            self.text.insert(END, dllFuncTestResponse+'\n')
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')
