from tkinter import *
import subprocess
import os

root=Tk()

CONNECTED=False

a=Label(root, text="Status: Checking for connected iDevice...")
a.pack()

csi = Entry(root, textvariable="Codesigning identity")
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
    l.see('end')

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
    global IPSW_READY
    jbbtn['state'] = 'disabled'
    log('building jailbreakd\n')
    log(f'using code sign identity: {csi.get()}\n')
    log('in directory, starting jailbreak\n')
    csIdentity = csi.get()
    if not csIdentity:
        csIdentity = "Apple Dev"
    log('Patching build.sh\n')
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
    log('build.sh patched successfully\n')
    log('compiling jailbreakd\n')
    try:
        subprocess.run(['/bin/bash', 'build.sh'], check=True, cwd='fugu14/arm/iOS/jailbreakd', shell=True)
    except subprocess.CalledProcessError as e:
        log(f'failed to build jailbreakd! exit code: {e.returncode}\n')
        exit(-1)
    log('Successfully built jailbreakd\n')
    log('getting jailbreakd cdhash\n')
    try:
        out = subprocess.run(['/usr/bin/codesign', '-dvvv', 'fugu14/arm/iOS/Fugu14App/Fugu14App/jailbreakd'], capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        pass
    cdhash = None
    out = out.stderr.decode('utf-8')
    for line in out.split('\n'):
        if line.startswith("CDHash="):
            cdhash = line[7:]
            break
    if cdhash is None:
        log(f'codesign did not output cdhash!\n')
        exit(-1)
    log(f'jailbreakd cdhash: {cdhash}\n')
    log('patching closures\n')
    
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

    log("patched\n")

    log("compiling jailbreak app\n")
    try:
        subprocess.run(['xcodebuild', '-scheme', 'Fugu14App', '-derivedDataPath', 'build'], check=True, cwd='fugu14/arm/iOS/Fugu14App', shell=True)
    except subprocess.CalledProcessError as e:
        log(f'failed to compile fugu14! exit code: {e.returncode}\n')
        log(f'if this was a code signing error, click Open XCode Project and ensure code signing is correct.\n')
        exit(-1)
    log('ready. please place your IPSW in **this folder**, and name it firmware.ipsw. when done, click Load IPSW below.\n')
    while not IPSW_READY:
        continue
    log('attempting to load ipsw\n')
    IPSW_READY = False
    try:
        subprocess.run(['mv', 'firmware.ipsw', 'firmware.zip'], shell=True)
    except subprocess.CalledProcessError as e:
        log(f'failed to extract firmware! exit code: {e.returncode}\n')
        exit(-1)
    try:
        if not os.path.exists('firmware/'):
            subprocess.run(['mkdir', 'firmware'])
        if not os.path.exists('mountd/'):
            subprocess.run(['mkdir', 'mountd'])
    except subprocess.CalledProcessError as e:
        log(f'failed to create extract/mount dirs! exit code: {e.returncode}\n')
        exit(-1)
    log('extracting ipsw file, this might take a while. please be patient!\n')
    try:
        subprocess.run(['unzip', 'firmware.zip', '-d', 'firmware/'], shell=True)
    except subprocess.CalledProcessError as e:
        log(f'failed to extract firmware! exit code: {e.returncode}\n')
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
        subprocess.run(['mount', mf, 'mountd/'], shell=True)
    except subprocess.CalledProcessError as e:
        log(f'failed to mount dmg! exit code: {e.returncode}\n')
        exit(-1)
    log(f'grabbing Spotlight.app\n')
    if not os.path.exists('mountd/Applications/Spotlight.app'):
        log(f'Spotlight does not exist!\n')
        exit(-1)
    try:
        subprocess.run(['cp', 'mountd/Applications/Spotlight.app', 'Spotlight.app'])
    except subprocess.CalledProcessError as e:
        log(f'failed to copy spotlight! exit code: {e.returncode}\n')
        exit(-1)
    try:
        subprocess.run(['umount', 'mountd'])
    except subprocess.CalledProcessError as e:
        log(f'failed to unmount drive! exit code: {e.returncode}\n')
        exit(-1)
    log('patching build_ipas.sh')
    try:
        subprocess.run(['cp', 'build_ipas_p.sh', 'fugu14/tools/build_ipas.sh'])
    except subprocess.CalledProcessError as e:
        log(f'failed to patch build_ipas! exit code: {e.returncode}\n')
        exit(-1)
    log('creating IPAs')
    try:
        subprocess.run(["/bin/bash", "build_ipas.sh", "../arm/iOS/Fugu14App/build/Build/Products/Release-iphoneos/Fugu14App.app", 'Spotlight.app'], check=True, cwd="fugu14/tools", shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create IPAs! Exit status: {e.returncode}\n")
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
