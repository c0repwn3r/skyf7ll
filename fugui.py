from tkinter import *
import tkinter.ttk
import subprocess
import os

deviceIdentifiers = {
    'iPhone1,1' : 'iPhone',
'iPhone1,2' : 'iPhone 3G',
'iPhone2,1' : 'iPhone 3GS',
'iPhone3,1' : 'iPhone 4',
'iPhone3,2' : 'iPhone 4 GSM Rev A',
'iPhone3,3' : 'iPhone 4 CDMA',
'iPhone4,1' : 'iPhone 4S',
'iPhone5,1' : 'iPhone 5 (GSM)',
'iPhone5,2' : 'iPhone 5 (GSM+CDMA)',
'iPhone5,3' : 'iPhone 5C (GSM)',
'iPhone5,4' : 'iPhone 5C (Global)',
'iPhone6,1' : 'iPhone 5S (GSM)',
'iPhone6,2' : 'iPhone 5S (Global)',
'iPhone7,1' : 'iPhone 6 Plus',
'iPhone7,2' : 'iPhone 6',
'iPhone8,1' : 'iPhone 6s',
'iPhone8,2' : 'iPhone 6s Plus',
'iPhone8,4' : 'iPhone SE (GSM)',
'iPhone9,1' : 'iPhone 7',
'iPhone9,2' : 'iPhone 7 Plus',
'iPhone9,3' : 'iPhone 7',
'iPhone9,4' : 'iPhone 7 Plus',
'iPhone10,1' :'iPhone 8',
'iPhone10,2' :'iPhone 8 Plus',
'iPhone10,3' : 'iPhone X Global',
'iPhone10,4' : 'iPhone 8',
'iPhone10,5' : 'iPhone 8 Plus',
'iPhone10,6' : 'iPhone X GSM',
'iPhone11,2' : 'iPhone XS',
'iPhone11,4' : 'iPhone XS Max',
'iPhone11,6' : 'iPhone XS Max Global',
'iPhone11,8' : 'iPhone XR',
'iPhone12,1' : 'iPhone 11',
'iPhone12,3' : 'iPhone 11 Pro',
'iPhone12,5' : 'iPhone 11 Pro Max',
'iPhone12,8' : 'iPhone SE 2nd Gen',
'iPhone13,1' : 'iPhone 12 Mini',
'iPhone13,2' : 'iPhone 12',
'iPhone13,3' : 'iPhone 12 Pro',
'iPhone13,4' : 'iPhone 12 Pro Max',
'iPhone14,2' : 'iPhone 13 Pro',
'iPhone14,3' : 'iPhone 13 Pro Max',
'iPhone14,4' : 'iPhone 13 Mini',
'iPhone14,5' : 'iPhone 13',
'iPad1,1' : 'iPad',
'iPad1,2' : 'iPad 3G',
'iPad2,1' : '2nd Gen iPad',
'iPad2,2' : '2nd Gen iPad GSM',
'iPad2,3' : '2nd Gen iPad CDMA',
'iPad2,4' : '2nd Gen iPad New Revision',
'iPad3,1' : '3rd Gen iPad',
'iPad3,2' : '3rd Gen iPad CDMA',
'iPad3,3' : '3rd Gen iPad GSM',
'iPad2,5' : 'iPad mini',
'iPad2,6' : 'iPad mini GSM+LTE',
'iPad2,7' : 'iPad mini CDMA+LTE',
'iPad3,4' : '4th Gen iPad',
'iPad3,5' : '4th Gen iPad GSM+LTE',
'iPad3,6' : '4th Gen iPad CDMA+LTE',
'iPad4,1' : 'iPad Air (WiFi)',
'iPad4,2' : 'iPad Air (GSM+CDMA)',
'iPad4,3' : '1st Gen iPad Air (China)',
'iPad4,4' : 'iPad mini Retina (WiFi)',
'iPad4,5' : 'iPad mini Retina (GSM+CDMA)',
'iPad4,6' : 'iPad mini Retina (China)',
'iPad4,7' : 'iPad mini 3 (WiFi)',
'iPad4,8' : 'iPad mini 3 (GSM+CDMA)',
'iPad4,9' : 'iPad Mini 3 (China)',
'iPad5,1' : 'iPad mini 4 (WiFi)',
'iPad5,2' : '4th Gen iPad mini (WiFi+Cellular)',
'iPad5,3' : 'iPad Air 2 (WiFi)',
'iPad5,4' : 'iPad Air 2 (Cellular)',
'iPad6,3' : 'iPad Pro (9.7 inch, WiFi)',
'iPad6,4' : 'iPad Pro (9.7 inch, WiFi+LTE)',
'iPad6,7' : 'iPad Pro (12.9 inch, WiFi)',
'iPad6,8' : 'iPad Pro (12.9 inch, WiFi+LTE)',
'iPad6,11' :' iPad (2017)',
'iPad6,12' :' iPad (2017)',
'iPad7,1' : 'iPad Pro 2nd Gen (WiFi)',
'iPad7,2' : 'iPad Pro 2nd Gen (WiFi+Cellular)',
'iPad7,3' : 'iPad Pro 10.5-inch 2nd Gen',
'iPad7,4' : 'iPad Pro 10.5-inch 2nd Gen',
'iPad7,5' : 'iPad 6th Gen (WiFi)',
'iPad7,6' : 'iPad 6th Gen (WiFi+Cellular)',
'iPad7,11' : 'iPad 7th Gen 10.2-inch (WiFi)',
'iPad7,12' : 'iPad 7th Gen 10.2-inch (WiFi+Cellular)',
'iPad8,1' : 'iPad Pro 11 inch 3rd Gen (WiFi)',
'iPad8,2' : 'iPad Pro 11 inch 3rd Gen (1TB, WiFi)',
'iPad8,3' : 'iPad Pro 11 inch 3rd Gen (WiFi+Cellular)',
'iPad8,4' : 'iPad Pro 11 inch 3rd Gen (1TB, WiFi+Cellular)',
'iPad8,5' : 'iPad Pro 12.9 inch 3rd Gen (WiFi)',
'iPad8,6' : 'iPad Pro 12.9 inch 3rd Gen (1TB, WiFi)',
'iPad8,7' : 'iPad Pro 12.9 inch 3rd Gen (WiFi+Cellular)',
'iPad8,8' : 'iPad Pro 12.9 inch 3rd Gen (1TB, WiFi+Cellular)',
'iPad8,9' : 'iPad Pro 11 inch 4th Gen (WiFi)',
'iPad8,10' : 'iPad Pro 11 inch 4th Gen (WiFi+Cellular)',
'iPad8,11' : 'iPad Pro 12.9 inch 4th Gen (WiFi)',
'iPad8,12' : 'iPad Pro 12.9 inch 4th Gen (WiFi+Cellular)',
'iPad11,1' : 'iPad mini 5th Gen (WiFi)',
'iPad11,2' : 'iPad mini 5th Gen',
'iPad11,3' : 'iPad Air 3rd Gen (WiFi)',
'iPad11,4' : 'iPad Air 3rd Gen',
'iPad11,6' : 'iPad 8th Gen (WiFi)',
'iPad11,7' : 'iPad 8th Gen (WiFi+Cellular)',
'iPad12,1' : 'iPad 9th Gen (WiFi)',
'iPad12,2' : 'iPad 9th Gen (WiFi+Cellular)',
'iPad14,1' : 'iPad mini 6th Gen (WiFi)',
'iPad14,2' : 'iPad mini 6th Gen (WiFi+Cellular)',
'iPad13,1' : 'iPad Air 4th Gen (WiFi)',
'iPad13,2' : 'iPad Air 4th Gen (WiFi+Cellular)',
'iPad13,4' : 'iPad Pro 11 inch 5th Gen',
'iPad13,5' : 'iPad Pro 11 inch 5th Gen',
'iPad13,6' : 'iPad Pro 11 inch 5th Gen',
'iPad13,7' : 'iPad Pro 11 inch 5th Gen',
'iPad13,8' : 'iPad Pro 12.9 inch 5th Gen',
'iPad13,9' : 'iPad Pro 12.9 inch 5th Gen',
'iPad13,10': 'iPad Pro 12.9 inch 5th Gen',
'iPad13,11' : 'iPad Pro 12.9 inch 5th Gen',
}

checkra1nVersions = ['12.0', '12.0.1', '12.1.1', '12.1.2', '12.1.3', '12.1.4', '12.2', '12.3', '12.3.1', '12.4',
                     '12.4.1', '13.0', '13.1', '13.1.2', '13.1.3', '13.2', '13.2.2', '13.2.3', '13.3', '13.4.1',
                     '13.5', '13.5.1', '13.6', '13.6.1', '13.7', '14.0', '14.0.1', '14.1', '14.2', '14.3', '14.4',
                     '14.4.1', '14.4.2', '14.5', '14.5.1', '14.6', '14.7', '14.7.1', '14.8']
checkra1nDevices = ['iPhone6,1','iPhone6,2','iPhone7,1','iPhone7,2','iPhone8,1','iPhone8,2','iPhone8,4',
                    'iPhone9,1','iPhone9,2','iPhone9,3','iPhone9,4','iPhone10,1','iPhone10,2','iPhone10,3',
                    'iPad4,1','iPad Air (WiFi)','iPad4,2','iPad4,3','iPad4,4','iPad4,5','iPad4,6','iPad4,7',
                    'iPad4,8','iPad4,9','iPad5,1','iPad5,2','iPad5,3','iPad5,4','iPad6,3','iPad6,4','iPad6,7',
                    'iPad6,8','iPad6,11','iPad6,12','iPad7,1','iPad7,2','iPad7,3','iPad7,4','iPad7,5','iPad7,6']

skyf7llVersions = ['14.4', '14.4.1', '14.4.2', '14.5', '14.5.1']
skyf7llDevices = ['iPhone11,2','iPhone11,4','iPhone11,6','iPhone11,8','iPhone12,1','iPhone12,3','iPhone12,5',
                  'iPhone12,8','iPhone13,1','iPhone13,2','iPhone13,3','iPhone13,4','iPhone14,2','iPhone14,3',
                  'iPhone14,4','iPhone14,5','iPad7,11','iPad7,12','iPad8,1','iPad8,2','iPad8,3','iPad8,4',
                  'iPad8,5','iPad8,6','iPad8,7','iPad8,8','iPad8,9','iPad8,10','iPad8,11','iPad8,12','iPad11,1',
                  'iPad11,2','iPad11,3','iPad11,4','iPad11,6','iPad11,7','iPad12,1','iPad12,2','iPad14,1',
                  'iPad14,2','iPad13,1','iPad13,2','iPad13,4','iPad13,5','iPad13,6','iPad13,7','iPad13,8',
                  'iPad13,9','iPad13,10','iPad13,11']

root=Tk()
root.wm_title('skyf7ll | checking dependencies (0/7)')

titlestatus = 'checking dependencies (0/7)'

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

error = Label(root, text='0/7 dependencies met, can not jailbreak', fg='red')
error.pack()

jbbtn = Button(root, text='Jailbreak', state='disabled')
jbbtn.pack()

recommendedjb = Label(root, text='recommended: none')
recommendedjb.pack()

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
    if (depsmet == 7):
        fg = 'green'
        txt = 'can'
        titlestat = 'ready'
    else:
        titlestat = f'checking dependencies ({depsmet}/7)'
    error['text'] = f'{depsmet}/7 dependencies met, {txt} jailbreak'
    error['fg'] = fg
    setTitleStatus(titlestat)
    root.update()

def getKey(key):
    return subprocess.run(['/usr/local/bin/ideviceinfo', '-k', key], capture_output=True).stdout.decode('utf-8')

def updateDevice():
    # get device ecid
    ECID = hex(int(getKey(ecidKey)[:-1]))
    deviceId = getKey(deviceIdKey)[:-1]
    deviceVersion = getKey(deviceVersionKey)[:-1]
    devtext = f'device: {deviceIdentifiers[deviceId]} (ECID: {ECID}), running version {deviceVersion}'
    device['text'] = devtext

def check_for_device():
    global devmet
    if libimobiledevice['text'] == 'libimobiledevice: installed!':
        if subprocess.run(['/usr/local/bin/idevice_id'], capture_output=True).stdout.decode('utf-8') != '':
            device['text'] = 'device: connected!'
            device['fg'] = 'green'
            devmet = True
            updateDevice()
            updatedeps()
        else:
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

    if os.path.exists('/usr/local/bin/idevice_id'):
        libimobiledevice['text'] = 'libimobiledevice: installed!'
        libimobiledevice['fg'] = 'green'
        libimobiledevicemet = True
        updatedeps()

root.after(500, fetch_deps)
root.after(500, check_for_device)
root.mainloop()
