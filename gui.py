from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog

class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Vars
        self.dll_path = None
        self.case_path = None
        self.service_name = None
        # Presets
        self.title("Win32 components testing")
        self.geometry("800x600")
        # Menu
        menubar = Menu(self)
        dllmenu = Menu(menubar, tearoff=0)
        dllmenu.add_command(label="Import .dll", command=self.getDllPath)
        dllmenu.add_command(label="Import test case", command=self.getTestCasePath)
        dllmenu.add_command(label="Run tests", command=self.runDllTests)
        servicemenu = Menu(menubar, tearoff=0)
        servicemenu.add_command(label="Get service by name", command=self.getServiceName)
        servicemenu.add_command(label="Import test case", command=self.getTestCasePath)
        servicemenu.add_command(label="Run tests", command=self.runServiceTests)
        menubar.add_cascade(label="DLL", menu=dllmenu)
        menubar.add_cascade(label="External win32 Services", menu=servicemenu)
        # Textarea
        self.text = Text(wrap="word")
        self.text.pack(fill=BOTH, expand=1)
        # Config
        self.config(menu=menubar)

    def getDllPath(self):
        try:
            filepath = filedialog.askopenfilename(
                title="Выбор файла",
                filetypes=[("Dynamic Link Library", "*.dll")]
            )
            if filepath != "":
                self.dll_path = filepath
                self.text.insert(END, f"dll lib {filepath} loaded\n")
        except Exception as e:
            self.text.insert(END, f"{e}\n")

    def getServiceName(self):
        try:
            serviceName = simpledialog.askstring("Get service name", "Enter the service name for the test\t\t\t")
            if serviceName != "":
                self.service_name = serviceName
                self.text.insert(END, f"service name is: {serviceName}\n")
        except Exception as e:
            self.text.insert(END, f"{e}\n")

    def getTestCasePath(self):
        try:
            filepath = filedialog.askopenfilename(
                title="Выбор файла",
                filetypes=[("JSON file", "*.json")]
            )
            if filepath != "":
                self.case_path = filepath
                self.text.insert(END, f"test case {filepath} loaded\n")
        except Exception as e:
            self.text.insert(END, f"{e}\n")

    def runDllTests(self):
        from t_tools import runThread
        from shedule import runProcess
        if not self.dll_path or not self.case_path:
            self.text.insert(END, "No dll modules or test case file imported\n")
            self.text.insert(END, ''.join("-" for i in range(32))+'\n')
        else:
            dllFuncTestResponse = runThread(runProcess, args=["./c_tools.py", self.dll_path, self.case_path])
            self.text.insert(END, dllFuncTestResponse+'\n')
            self.text.insert(END, ''.join("-" for i in range(32))+'\n')

    def runServiceTests(self):
        from t_tools import runThread
        from shedule import runProcess
        if not self.service_name or not self.case_path:
            self.text.insert(END, "No dll modules or test case file imported\n")
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')
        else:
            serviceFuncTestResponse = runThread(runProcess, args=["./p_tools.py", self.service_name, self.case_path])
            self.text.insert(END, serviceFuncTestResponse+'\n')
            self.text.insert(END, ''.join("-" for i in range(50))+'\n')
