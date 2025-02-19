from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Vars
        self.dll_path = None
        self.case_path = None
        # Presets
        self.title("DLL Testing App")
        self.geometry("640x480")
        # Menu
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load .dll", command=self.getDllPath)
        filemenu.add_command(label="Load case file", command=self.getTestCasePath)
        runmenu = Menu(menubar, tearoff=0)
        runmenu.add_command(label="Run tests", command=self.runDllTests)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Run", menu=runmenu)
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
        from c_tools import dllFuncTest
        from t_tools import runThread
        if not self.dll_path or not self.case_path:
            self.text.insert(END, "No dll modules or test case file imported\n")
        else:
            dllFuncTestResponse = runThread(dllFuncTest, [self.dll_path, self.case_path])
            self.text.insert(END, '\n'.join([str(response) for response in dllFuncTestResponse])+'\n')
