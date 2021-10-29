from tkinter import *
import tkinter.ttk
import subprocess
import os

root=Tk()

csidentity = Label(root, text='csIdentity: none', fg='red')
csimet = True
csidentity.pack()

device = Label(root, text='device: not connected', fg='red')
devmet = True
device.pack()

xcode = Label(root, text='xcode: not installed', fg='red')
xcode.pack()

usbmuxd = Label(root, text='usbmuxd: not installed', fg='red')
usbmuxd.pack()

ideviceinstaller = Label(root, text='ideviceinstaller: not installed', fg='red')
ideviceinstaller.pack()

libimobiledevice = Label(root, text='libimobiledevice: not installed', fg='red')
libimobiledevice.pack()

homebrew = Label(root, text='homebrew: not installed', fg='red')
homebrew.pack()

error = Label(root, text='0/7 dependencies met, can not jailbreak', fg='red')
error.pack()

jbbtn = Button(root, text='Jailbreak', state='disabled')
jbbtn.pack()

status = Label(root, text='status: waiting for dependencies')
status.pack()

progress = tkinter.ttk.Progressbar(root, length=200)
progress.pack()

depsmet = 0

def get_codesign_identity():
    # this thing is a freakin complicated mess
    out = subprocess.run(['security', 'find-identity'], check=True, capture_output=True)
    csIdentity=None
    foundInvalid=True
    for line in out.stdout.decode('utf-8').split('\n'):
        if line.startswith('  1) '):
            # yay there's a valid identity
            if(foundInvalid):
                foundInvalid=False
                continue
            csIdentity = line[47:-1]
            print(f'dbg: found codesign identity {csIdentity}')
    return csIdentity

def updatedeps():
    txt = 'can not'
    fg = 'red'
    if (depsmet == 7):
        fg = 'green'
        txt = 'can'
    error['text'] = f'{depsmet}/7 dependencies met, {txt} jailbreak'
    error['fg'] = fg
    root.update()

def check_for_device():
    if libimobiledevice['text'] == 'libimobiledevice: installed!':
        if subprocess.run(['/usr/local/bin/idevice_id'], capture_output=True).stdout.decode('utf-8') != '':
            device['text'] = 'device: connected!'
            device['fg'] = 'green'
            depsmet += 1
            updatedeps()
        else:
            

def fetch_deps():
    global depsmet
    identity = get_codesign_identity()
    if identity != None:
        csidentity['text'] = f'csIdentity: {identity}'
        csidentity['fg'] = 'green'
        depsmet += 1
        updatedeps()

    if os.path.exists('/Applications/Xcode.app'):
        xcode['text'] = 'xcode: installed!'
        xcode['fg'] = 'green'
        depsmet += 1
        updatedeps()

    if os.path.exists('/usr/local/bin/brew'):
        homebrew['text'] = 'homebrew: installed!'
        homebrew['fg'] = 'green'
        depsmet += 1
        updatedeps()
        if 'No avaliable' not in subprocess.run(['/usr/local/bin/brew', 'list', 'usbmuxd'], capture_output=True).stdout.decode('utf-8'):
            usbmuxd['text'] = 'usbmuxd: installed!'
            usbmuxd['fg'] = 'green'
            depsmet += 1
            updatedeps()
        if 'No avaliable' not in subprocess.run(['/usr/local/bin/brew', 'list', 'ideviceinstaller'], capture_output=True).stdout.decode('utf-8'):
            ideviceinstaller['text'] = 'ideviceinstaller: installed!'
            ideviceinstaller['fg'] = 'green'
            depsmet += 1
            updatedeps()

    if os.path.exists('/usr/local/bin/idevice_id'):
        libimobiledevice['text'] = 'libimobiledevice: installed!'
        libimobiledevice['fg'] = 'green'
        depsmet += 1
        updatedeps()

root.after(500, fetch_deps)
root.mainloop()
