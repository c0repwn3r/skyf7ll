from tkinter import *
import tkinter.ttk
from tkinter.messagebox import showinfo
import subprocess
import os
import time

from devices import *

from multiprocessing.connection import Client

root=Tk()
root.wm_title('skyf7ll | checking dependencies (0/8)')

titlestatus = 'checking dependencies (0/8)'

def setTitleStatus(newstatus):
    global titlestatus
    titlestatus = newstatus
    root.wm_title(f'skyf7ll | {titlestatus}')

csidentity = Label(root, text='csIdentity: none', fg='red')
csimet = False
csidentity.pack()

device = Label(root, text='device: not connected', fg='red')
devmet = False
device.pack()

xcode = Label(root, text='xcode: not installed', fg='red')
xcodemet = False
xcode.pack()

usbmuxd = Label(root, text='usbmuxd: not installed', fg='red')
usbmuxdmet = False
usbmuxd.pack()

ideviceinstaller = Label(root, text='ideviceinstaller: not installed', fg='red')
ideviceinstallermet = False
ideviceinstaller.pack()

libimobiledevice = Label(root, text='libimobiledevice: not installed', fg='red')
libimobiledevicemet = False
libimobiledevice.pack()

homebrew = Label(root, text='homebrew: not installed', fg='red')
homebrewmet = False
homebrew.pack()

fastlane = Label(root, text='fastlane: not installed', fg='red')
fastlanemet = False
fastlane.pack()

error = Label(root, text='0/7 dependencies met, can not jailbreak', fg='red')
error.pack()

jbbtn = Button(root, text='Jailbreak', state='disabled')
jbbtn.pack()

cjb = Label(root, text='recommended: none')
cjb.pack()
jbtouse = 'none'

status = Label(root, text='status: waiting for dependencies')
status.pack()

progress = tkinter.ttk.Progressbar(root, length=200)
progress.pack()

ECID = ''
deviceId = ''
deviceFriendlyName = ''
deviceVersion=''

ecidKey = 'UniqueChipID'
deviceIdKey='ProductType'
deviceVersionKey='ProductVersion'

use_skyfall = False
checkra1n_dwl = 'https://assets.checkra.in/downloads/macos/754bb6ec4747b2e700f01307315da8c9c32c8b5816d0fe1e91d1bdfc298fe07b/checkra1n%20beta%200.12.4.dmg'

def setProgress(val, maxv):
    progress['maximum'] = maxv
    progress['value'] = val
    root.update_idletasks()

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
    global csimet
    global devmet
    global xcodemet
    global usbmuxdmet
    global ideviceinstallermet
    global libimobiledevicemet
    global homebrewmet
    global fastlanemet
    txt = 'can not'
    fg = 'red'
    titlestat = 'checking dependencies'
    depsmet = 0
    if (csimet):
        depsmet += 1
    if (devmet):
        depsmet += 1
    if (xcodemet):
        depsmet += 1
    if (usbmuxdmet):
        depsmet += 1
    if (ideviceinstallermet):
        depsmet += 1
    if (libimobiledevicemet):
        depsmet += 1
    if (homebrewmet):
        depsmet += 1
    if (fastlanemet):
        depsmet += 1
    if (depsmet == 8):
        fg = 'green'
        txt = 'can'
        titlestat = 'ready'
        setProgress(0, 0)
    else:
        titlestat = f'checking dependencies ({depsmet}/8)'
        jbbtn['command'] = None
        jbbtn['state'] = 'disabled'
        setProgress(8*depsmet/8, 8)
    error['text'] = f'{depsmet}/8 dependencies met, {txt} jailbreak'
    error['fg'] = fg
    setTitleStatus(titlestat)
    root.update()

def getKey(key):
    return subprocess.run(['/usr/local/bin/ideviceinfo', '-k', key], capture_output=True).stdout.decode('utf-8')

def setprog(stat, stage):
    global status
    global progress
    status['text'] = f'status: {stat}'
    progress['maximum'] = 12
    progress['value'] = 12*stage/12
    root.update_idletasks()

def skyfall_run():
    # stages: command server start, command server conn, jailbreakd patch, jailbreakd compile, fugu patch, fugu compile, ipsw extract, ipa build, setup install, setup, exploit install, exploit
    # 12 stages
    jbbtn['state'] = 'disabled'
    status['text'] = 'status: prepping'
    setTitleStatus('jailbreaking')
    setprog('starting command server', 1)
    # start command server
    wrapperscript = 'osascript -e "tell application \"Terminal\" to do script \"cd $PWD && python3 cmdserver.py\""'
    subprocess.Popen(wrapperscript.split(), cwd=os.path.dirname(os.path.realpath(__file__)))
    setprog('waiting for command server', 1)
    showinfo('Start command server', 'Please double-click on STAGE2.command at this time. Click Ok when you see the text `listening on 6151`')
    address = ('localhost', 6151)
    try:
        conn = Client(address, authkey=b'skyf7ll-ipc')
    except:
        setprog('failed to connect to command server!', 0)
        jbbtn['state'] = 'normal'
        setTitleStatus('failed')
        return
    setprog('connected to command server', 2)
    setprog('patching jailbreakd')
def checkrain_run():
    pass

def updateChosenJb():
    global jbtouse
    global use_skyfall
    if jbtouse == 'skyf7ll':
        use_skyfall = True
        cjb['text'] = 'recommended: skyf7ll'
        jbbtn['state'] = 'normal'
        jbbtn['command'] = skyfall_run
        status['text'] = 'status: ready to jailbreak'
    elif jbtouse == 'checkra1n':
        cjb['text'] = 'recommended: checkra1n'
        jbbtn['state'] = 'normal'
        status['text'] = 'status: ready to jailbreak'
        jbbtn['command'] = checkrain_run

def updateDevice():
    global ECID
    global deviceId
    global deviceVersion
    global jbtouse
    # get device ecid
    ECID = hex(int(getKey(ecidKey)[:-1]))
    deviceId = getKey(deviceIdKey)[:-1]
    deviceVersion = getKey(deviceVersionKey)[:-1]
    devtext = f'device: {deviceIdentifiers[deviceId]} (ECID: {ECID}), running version {deviceVersion}'
    device['text'] = devtext
    # check recommended jailbreaks
    if deviceId in skyf7llDevices and deviceVersion in skyf7llVersions:
        jbtouse = 'skyf7ll'
        updateChosenJb()
        return
    if deviceId in checkra1nDevices and deviceVersion in checkra1nVersions:
        jbtouse = 'checkra1n'
        updateChosenJb()
        return

def check_for_device():
    global devmet
    if libimobiledevice['text'] == 'libimobiledevice: installed!':
        out = subprocess.run(['/usr/local/bin/idevice_id'], capture_output=True).stdout.decode('utf-8')
        if devmet == False and out != '':
            device['text'] = 'device: connected!'
            device['fg'] = 'green'
            devmet = True
            updateDevice()
            updatedeps()
        elif out == '':
            device['text'] = 'device: not connected'
            device['fg'] = 'red'
            devmet = False
            updatedeps()
    root.after(500, check_for_device)

def fetch_deps():
    global csimet
    global devmet
    global xcodemet
    global usbmuxdmet
    global ideviceinstallermet
    global libimobiledevicemet
    global homebrewmet
    global gemmet
    global fastlanemet
    identity = get_codesign_identity()
    if identity != None:
        csidentity['text'] = f'csIdentity: {identity}'
        csidentity['fg'] = 'green'
        csimet = True
        updatedeps()

    if os.path.exists('/Applications/Xcode.app'):
        xcode['text'] = 'xcode: installed!'
        xcode['fg'] = 'green'
        xcodemet = True
        updatedeps()

    if os.path.exists('/usr/local/bin/brew'):
        homebrew['text'] = 'homebrew: installed!'
        homebrew['fg'] = 'green'
        homebrewmet = True
        updatedeps()
        if 'No avaliable' not in subprocess.run(['/usr/local/bin/brew', 'list', 'usbmuxd'], capture_output=True).stdout.decode('utf-8'):
            usbmuxd['text'] = 'usbmuxd: installed!'
            usbmuxd['fg'] = 'green'
            usbmuxdmet = True
            updatedeps()
        if 'No avaliable' not in subprocess.run(['/usr/local/bin/brew', 'list', 'ideviceinstaller'], capture_output=True).stdout.decode('utf-8'):
            ideviceinstaller['text'] = 'ideviceinstaller: installed!'
            ideviceinstaller['fg'] = 'green'
            ideviceinstallermet = True
            updatedeps()
        if 'No avaliable' not in subprocess.run(['/usr/local/bin/brew', 'list', 'fastlane'], capture_output=True).stdout.decode('utf-8'):
            fastlane['text'] = 'fastlane: installed!'
            fastlane['fg'] = 'green'
            fastlanemet = True
            updatedeps()

    if os.path.exists('/usr/local/bin/idevice_id'):
        libimobiledevice['text'] = 'libimobiledevice: installed!'
        libimobiledevice['fg'] = 'green'
        libimobiledevicemet = True
        updatedeps()

root.after(500, fetch_deps)
root.after(500, check_for_device)
root.mainloop()
