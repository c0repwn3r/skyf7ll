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

IPSW_READY = False

def loadipsw():
    IPSW_READY=True
    return

i = Button(root, text='Load IPSW', bd='5', command=loadipsw)
i.pack()

def openxcproj():
    os.system('xed fugu14/arm/iOS/Fugu14App/Fugu14App.xcodeproj')

jbbtn = Button(root, text='Jailbreak',bd='5',state='disabled')
xcodebtn = Button(root, text='Open XCode Project', bd='5', command=openxcproj)
xcodebtn.pack()

def run_jb():
    jbbtn['state'] = 'disabled'
    log('building jailbreakd')
    log(f'using code sign identity: {codesign_identity}')
    log('in directory, starting jailbreak')
    csIdentity = CODESIGN_IDENTITY
    if not csIdentity:
        csIdentity = "Apple Dev"
    prlogint('Patching build.sh')
    with open('fugu14/arm/iOS/jailbreakd/build.sh', 'r') as f:
        build_sh = f.read()
    lines = []
    for line in build_sh.split("\n"):
        if line.startswith("CODESIGN_IDENTITY="):
            lines.append(f'CODESIGN_IDENTITY="{csIdentity}"')
        else:
            lines.append(line)

    with open("fugu14/arm/iOS/jailbreakd/build.sh", "w") as f:
        f.write("\n".join(lines))
    log('build.sh patched successfully')
    log('compiling jailbreakd')
    try:
        subprocess.run(['/bin/bash', 'build.sh'], check=True, cwd='fugu14/arm/iOS/jailbreakd')
    except subprocess.CalledProcessError as e:
        log(f'failed to build jailbreakd! exit code: {e.returncode}')
        exit(-1)
    log('Successfully built jailbreakd')
    log('getting jailbreakd cdhash')
    try:
        out = subprocess.run(['/usr/bin/codesign', '-dvvv', 'fugu14/arm/iOS/Fugu14App/Fugu14App/jailbreakd'], capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        log(f'failed to get cdhash! exit code: {e.returncode}')
        log(f'codesign stdout: {e.stdout}')
        log(f'codesign stderr: {e.stderr}')
        exit(-1)
    cdhash = None
    out = out.stderr.decode('utf-8')
    for line in out.split('\n'):
        if line.startswith("CDHash="):
            cdhash = line[7:]
            break
    if cdhash is None:
        log(f'codesign did not output cdhash!')
        exit(-1)
    log(f'jailbreakd cdhash: {cdhash}')
    log('patching closures')
    
    with open('fugu14/arm/iOS/Fugu14App/Fugu14App/closures.swift', 'r') as f:
        closure_swift = f.read()
    
    lines = []
    for line in closure_swift.split("\n"):
        if line.startswith('        try simpleSetenv("JAILBREAKD_CDHASH", '):
            lines.append (f'        try simpleSetenv("JAILBREAKD_CDHASH", "{cdhash}")')
        else:
            lines.append(line)

    with open("fugu14/arm/iOS/Fugu14App/Fugu14App/closures.swift", "w") as f:
        f.write("\n".join(lines))

    log("patched")

    log("compiling jailbreak app")
    try:
        subprocess.run(['xcodebuild', '-scheme', 'Fugu14App', '-derivedDataPath', 'build'], check=True, cwd='fugu14/arm/iOS/Fugu14App')
    except subprocess.CalledProcessError as e:
        log(f'failed to compile fugu14! exit code: {e.returncode}')
        log(f'if this was a code signing error, click Open XCode Project and ensure code signing is correct.')
        exit(-1)
    log('ready. please place your IPSW in **this folder**, and name it firmware.ipsw. when done, click Load IPSW below.')
    while not IPSW_READY:
        continue
    log('attempting to load ipsw')
    IPSW_READY = False
    try:
        subprocess.run(['mv', 'firmware.ipsw', 'firmware.zip'])
    except subprocess.CalledProcessError as e:
        log(f'failed to extract firmware! exit code: {e.returncode}')
        exit(-1)
    try:
        if not os.path.exists('firmware/'):
            subprocess.run(['mkdir', 'firmware'])
        if not os.path.exists('mountd/'):
            subprocess.run(['mkdir', 'mountd'])
    except subprocess.CalledProcessError as e:
        log(f'failed to create extract/mount dirs! exit code: {e.returncode}')
        exit(-1)
    log('extracting ipsw file, this might take a while. please be patient!')
    try:
        subprocess.run(['unzip', 'firmware.zip', '-d', 'firmware/'])
    except subprocess.CalledProcessError as e:
        log(f'failed to extract firmware! exit code: {e.returncode}')
        exit(-1)
    path = os.path.abspath('firmware/')
    size = 0
    msize = 0
    mf = ''
    for folder, subfolder, files in os.walk(path):
        for file in files:
        size = os.stat(os.path.join( folder, file  )).st_size
        if size>max_size:
            max_size = size
            max_file = os.path.join(folder, file)
    log(f'mounting {mf}')
    try:
        subprocess.run(['mount', mf, 'mountd/'])
    except subprocess.CalledProcessError as e:
        log(f'failed to mount dmg! exit code: {e.returncode}')
        exit(-1)
    log(f'grabbing Spotlight.app')
    if not os.path.exists('mountd/Applications/Spotlight.app'):
        log(f'Spotlight does not exist!')
        exit(-1)
    try:
        subprocess.run(['cp', 'mountd/Applications/Spotlight.app', 'Spotlight.app'])
    except subprocess.CalledProcessError as e:
        log(f'failed to copy spotlight! exit code: {e.returncode}')
        exit(-1)
    try:
        subprocess.run(['umount', 'mountd'])
    except subprocess.CalledProcessError as e:
        log(f'failed to unmount drive! exit code: {e.returncode}')
        exit(-1)
    log('creating IPAs')
    try:
        subprocess.run(["/bin/bash", "build_ipas.sh", "../arm/iOS/Fugu14App/build/Build/Products/Release-iphoneos/Fugu14App.app", mntPath], check=True, cwd="fugu14/tools")
    except subprocess.CalledProcessError as e:
    print(f"Failed to create IPAs! Exit status: {e.returncode}")
    exit(-1)

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
