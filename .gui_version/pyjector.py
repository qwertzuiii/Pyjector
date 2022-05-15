import sys, os
from unicodedata import name
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5 import uic, QtTest
from PyQt5.QtGui import QIcon
import phasto as ph
import pyinj
import psutil
import easygui as ez
from box import Ui_MainWindow as boxmain

def aubooter():
    tempboot = 'resources/tmp/boot'
    try:
        os.makedirs(tempboot)  # Creates directories to read jsons
    except: pass
    ph.file.unzip('resources/boot.bin', tempboot)  # Unzip boot.bin [boot info's, its a zip :)]
    returncfg = ph.file.read_json(tempboot + '/config.json')
    returnver = ph.file.read(tempboot + '/version.v')

    try:
        os.remove(tempboot + '/config.json')
        os.remove(tempboot + '/version.v')
        os.removedirs(tempboot)  # Deletes directories because no one needs it
    except: pass

    return returncfg, returnver

def get_pid(executableName):
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if executableName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    for elem in listOfProcessObjects:
        processID = elem['pid']
        processName = elem['name']
    
    return processID, processName

text_status_def = 'IDLE'

text_status_nopselect = 'No process selected!'
text_status_nopfound = 'No process found!'

text_status_nodselect = 'No dll selected!'
text_status_nodfound = 'No dll found!'

class MainApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        self.config, self.version = aubooter()

        uic.loadUi(self.config['ii'], self)  # ui file load
        self.setWindowIcon(QIcon(self.config['getico']))  # Icon Loading
        self.setWindowTitle('PyJector v' + self.version)

        self.st.setText(text_status_def)

        self.inj.clicked.connect(self.inject_time)
        self.dllb.clicked.connect(self.browsedll)

    def inject_time(self):
        nameofprocess = self.gameprocess.text()
        dll = self.dll.text()

        if nameofprocess != '':
            try:
                pid, pname = get_pid(nameofprocess)
            except:
                self.openbox(text_status_nopfound)
                self.chst(text_status_nopfound)
                return
        else:
            self.openbox(text_status_nopselect)
            self.chst(text_status_nopselect)
            return

        if dll != '':
            pass
        else:
            self.openbox(text_status_nodselect)
            self.chst(text_status_nodselect)
            return
        
        if os.path.exists(dll):
            pass
        else:
            self.openbox(text_status_nodfound)
            self.chst(text_status_nodfound)
            return

        print(pid, pname, dll)

        pyinj.inject(pid, dll)
        self.openbox('Successfully injected')
        
        #ez.msgbox('Imported successfully!', 'Pyjector - Inject successfull')
    

    def browsedll(self):
        i = ez.fileopenbox('Open DLL for inject', 'PyJector', '*.dll')
        self.dll.setText(i)


    def wait(self, i):
        QtTest.QTest.qWait(i)
    
    def chst(self, text):
        self.st.setText(text)
        self.wait(1000)
        self.st.setText(text_status_def)
    
    def openbox(self, text):
        ph.file.write('resources/i.nfo', text)
        self.thatbox = QMainWindow()
        self.getui = boxmain()
        self.getui.setupUi(self.thatbox)
        self.thatbox.show()
        os.remove('resources/i.nfo')
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp()
    appMain.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Exiting...')