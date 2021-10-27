from tkinter import *
import subprocess
import os

root=Tk()

CONNECTED=False

a=Label(root, text="Status: Checking for connected iDevice...")
a.pack()

l=Text(root)
l.pack(expand=True)
l.insert('end', 'Checking for connected iDevice...')
l['state']='disabled'

def log(msg):
    a['text'] = f'Status: {msg}'
    l['state']='normal'
    l.insert('end', msg)
    l['state']='disabled'

jbbtn = Button(root, text='Jailbreak',bd='5',state='disabled')

def run_jb():
    jbbtn['state'] = 'disabled'
    log('(depchecker) checking for dependencies: usbmuxd')
    try:
        if (subprocess.check_output(['ls', '/var/run/usbmuxdd']).decode('utf-8') != '/var/run/usbmuxd'):
            log('error: usbmuxd not installed or running')
            return
    except subprocess.CalledProcessError as e:
        log(f'error: usbmuxd not installed or running (error code: {e.returncode})')
        return
    log('(depchecker) checking for dependencies: ideviceinstall')

jbbtn['command'] = run_jb
jbbtn.pack()

def device_status():
    if (subprocess.check_output(['/usr/local/bin/idevice_id', '-l']).decode('utf-8') != ""):
        log('Connected! Ready to jailbreak.')
        jbbtn['state']='normal'
    else:
        log('Checking for connected iDevice...')
        jbbtn['state']='disabled'
    root.after(500, device_status)

root.after(500, device_status)
root.mainloop()

print("test")
