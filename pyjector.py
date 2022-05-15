import os, time
from resources.plugin import phasto as ph
from pyinjector import inject as injo
import psutil
import easygui as ez

px = f'{ph.clr.yellow}<{ph.clr.red}PyJector{ph.clr.yellow}> {ph.clr.green}'  # Prefix to use in every text


def pln(text_to_print, prefix=px):
    print(prefix + text_to_print)

def inln(text_to_print, prefix=px):
    return input(prefix + text_to_print)


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

def get_pid(processName):
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects

# Booting up
ph.os.clear()
pln('Booting up...')
cfg, bootver = aubooter()
if cfg['boot_modded']:
    o = ' %s(%sModded Boot%s)' % (ph.clr.yellow, ph.clr.red, ph.clr.yellow)
else: o = ''
pln('Booted with version ' + bootver + o)
time.sleep(1)
ph.next_line(1)

# METHODS
with open('resources/method.mstr', 'r') as f:
    for line in f.readlines():
        data = line.rstrip()
        method_list = data.split("|")

loop_methods = True
while loop_methods:
    ph.os.clear()
    o = 0
    pln('Select:\n')
    for i in range(len(method_list)):
        pln(method_list[o])
        o += 1

    selection = ph.os.one_input()

    # Selections

    if selection == b'1':
        processselect = True

        while processselect:
            ph.next_line(1)
            nameofprocess = inln('Name of Process (like in taskmanager):  ')
            pid = get_pid(nameofprocess)

            for elem in pid:
                processID = elem['pid']
                processName = elem['name']
                processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
            getretry = False

            try:
                ph.next_line(1)
                pln('Found PID for process: ' + str(processID) + ' as ' + processName + ', created process: ' + str(processCreationTime))
                ph.next_line(1)
            except:
                ph.next_line(1)
                pln('Process %s not found! Press a key to retry' % nameofprocess)
                ph.os.one_input()
                getretry = True

            if getretry == False:
                dllselect = True

                while dllselect:
                    dllgetpath = True

                    while dllgetpath:
                        dllpath = ez.fileopenbox('DLL to Inject')
                    
                        if dllpath == None:
                            pass
                        else: dllgetpath = False

                    
                    yea = ez.ynbox('Process: %s\nDLL: %s\nRight?' % (processName, dllpath), 'PyJector')

                    if yea == True:
                        processselect = False
                        dllselect = False
                    elif yea == None:
                        pass
                    else:
                        dllselect = False

        injo(processID, str(dllpath))
        ph.next_line(1)
        ez.msgbox('Successfully injected to %s!' % processName, 'PyJector')
        pln('Successfully injected!\n\n[PROCESS: %s, %s DLL: %s]' % (nameofprocess, pid, dllpath))
        time.sleep(2)

    if selection == b'q': loop_methods = False



# Automatic end
print(ph.clr.resc)