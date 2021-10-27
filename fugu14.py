from tkinter import *
import subprocess
import os

root=Tk()

CONNECTED=False

a=Label(root, text="Status: Checking for connected iDevice...")
a.pack()

codesign_identity = 'Put code signing identity here!'
csi = Entry(root, textvariable=codesign_identity)
csi.pack()

b = Button(root, text='Update CSI', bd='5')

l=Text(root)
l.pack(expand=True)
l.insert('end', 'Avaliable code signing identities:\n')
l.insert('end', subprocess.check_output(['security', 'find-identity']))
l.insert('end', 'Checking for connected iDevice...\n')
l['state']='disabled'

def printmsg(msg):
    l['state']='normal'
    l.insert('end', msg)
    l['state']='disabled'

def log(msg):
    a['text'] = f'Status: {msg}'
    l['state']='normal'
    l.insert('end', msg)
    l['state']='disabled'

def refreshcsi():
    log('Refreshing code signing identities...')
    printmsg(subprocess.check_output(['security', 'find-identity']))
    log('Refresh successful')

b['command'] = refreshcsi
b.pack()

def openxcproj():
    os.system('xed fugu14/arm/iOS/Fugu14App/Fugu14App.xcodeproj')

jbbtn = Button(root, text='Jailbreak',bd='5',state='disabled')
xcodebtn = Button(root, text='Open XCode Project', bd='5', command=openxcproj)
xcodebtn.pack()

def run_jb():
    jbbtn['state'] = 'disabled'
    log('building jailbreakd')
    os.chdir('fugu14')
    log(f'using code sign identity: {codesign_identity}')
    log('in directory, starting jailbreak')

jbbtn['command'] = run_jb
jbbtn.pack()

def device_status():
    global CONNECTED
    if(CONNECTED):
        return
    if (subprocess.check_output(['/usr/local/bin/idevice_id', '-l']).decode('utf-8') != ""):
        CONNECTED=True
        log('Connected! Ready to jailbreak.\n')
        jbbtn['state']='normal'
    else:
        a['text'] = 'Checking for connected iDevice...'
        CONNECTED=False
        jbbtn['state']='disabled'
    root.after(500, device_status)

root.after(500, device_status)
root.mainloop()

print("test")
