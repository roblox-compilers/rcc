# simple script to download RCC
# packages: shutil lupa requests xmltodict inquirer
# cli: pyinstaller
import os, subprocess

def installPip(pkg):
    try:
        exec(f"import {pkg}")
        print(f"{pkg} already installed")
    except:
        print(f"installing {pkg}...")
        os.system(f"pip install {pkg}")
        print(f"installed {pkg}")
        
def checkCli(cli):
    suc = subprocess.call(f"{cli} -v", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return suc == 0

if not checkCli("pip"):
    print("--------------------")
    print("failure: pip not installed")
    exit(1)
    
print("INSTALLING DEPENDENCIES...")
for i in ["shutil", "lupa", "requests", "xmltodict", "inquirer"]:
    installPip(i)
    
if not checkCli("pyinstaller"):
    os.system("pip install pyinstaller")
    
print("COMPILING...")
os.system("pyinstaller rcc.py --onefile")

print("INSTALLING...")
os.chdir("dist")

plat = input("windows or unix? (w/u)  ").lower() == "w"
for i in os.listdir():
    if plat:
        path = "C:\Windows\system32"
    else:
        path = "/usr/local/bin"
        
    # move to path
    os.rename(i, os.path.join(path, i))
    print(f"installed {i} to {path}")