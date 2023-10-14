"""
Handles all the packages
"""
import os, sys
import log
try:
    import requests
except:
    log.error("requests not installed, please install it using 'pip install requests'")
def qts():
    if input("\033[1;33mreccomendation \033[0m\033[90mCORE rcc:\033[0m would you like to install qts alongside rbxts? (y/n)  ").lower() == "y":
        install("qts")
    else:
        return True
    
def installrbxts():
    print("\033[1;33minfo \033[0m\033[90mCORE rcc:\033[0m rbxts requires npm to be installed")
    os.system("npm install -g typescript")
    os.system("npm install -g @rbxts/rbxts-cli")
    
def installincludes():
    log.info("installing roblox-c includes...")
    contents = requests.get("https://raw.githubusercontent.com/roblox-compilers/roblox-c/main/src/rbx.h").text
    if sys.platform == "win32":
        with open(input("Please enter the path to your C and C++ include folder: ") + "\\rbx.h", "w") as f:
            f.write(contents)   
    else:
        with open("/usr/local/include/rbx.h", "w") as f:
            f.write(contents)
            
def notact():
    log.error("not available")
    
exec = {
    "roblox-py": {
        "repo": "roblox-compilers/roblox-py",
        "darwin": "rbxpy",
        "win32": "rbxpy.exe",
        "special": None
    }, 
    "roblox-c": {
        "repo": "roblox-compilers/roblox-c",
        "darwin": "rbxc",
        "win32": "rbxc.exe",
        "special": notact
    }, 
    "roblox-cs": {
        "repo": "roblox-compilers/roblox-cs",
        "darwin": "rbxcs",
        "win32": "rbxcs.exe",
        "special": notact
    },
    "roblox-ts": {
        "repo": "roblox-compilers/roblox-ts",
        "darwin": "rbxtsc",
        "win32": "rbxtsc.exe",
        "special": qts,
        "specialin": installrbxts
    },
    "roblox-kt": {
        "repo": "roblox-compilers/roblox-kt",
        "darwin": "rbxkt",
        "win32": "rbxkt.exe",
        "special": notact
    },
    "qts": {
        "repo": "roblox-compilers/qts",
        "darwin": "qts",
        "win32": "qts.exe",
        "special": None
    },
    "roblox-wasm": {
        "repo": "roblox-compilers/roblox-wasm",
        "darwin": "rbxwasm",
        "win32": "rbxwasm.exe",
        "special": None
    },
    "rcc": {
        "repo": "roblox-compilers/rcc",
        "darwin": "rcc",
        "win32": "rcc.exe",
        "special": None
    },
}

relative = {
    # RBX
    "rbxpy": "roblox-py",
    "rbxc": "roblox-c",
    "rbxcs": "roblox-cs",
    "rbxts": "roblox-ts",
    "rbxkt": "roblox-kt",
    "rbxwasm": "roblox-wasm",
    
    # Other
    "qts": "qts",
    "wasm": "roblox-wasm",
    "rcc": "rcc",
    
    # roblox-
    "roblox-py": "roblox-py",
    "roblox-c": "roblox-c",
    "roblox-cs": "roblox-cs",
    "roblox-ts": "roblox-ts",
    "roblox-kt": "roblox-kt",
    "roblox-wasm": "roblox-wasm",
}

def install(pkg):
    if (pkg in relative):
        if exec[relative[pkg]]["special"]:
            exec[relative[pkg]]["special"]()
        if "specialin" in exec[relative[pkg]]:
            exec[relative[pkg]]["specialin"]()
        else:
            path = f"https://github.com/{exec[relative[pkg]]['repo']}/releases/latest/download/{exec[relative[pkg]][sys.platform] or log.error('platform not supported')}"
                
            log.info(f"downloading {pkg}...")
            r = requests.get(path)
            with open(exec[relative[pkg]][sys.platform], "wb") as f:
                f.write(r.content)
                
            log.info(f"installing {pkg}...")
            bin(exec[relative[pkg]][sys.platform])
            
    else:
        log.error(f"package '{pkg}' not found")
            
            
def bin(file):
    # Move the file to /usr/bin in macOS and Linux, and to C:\win32dows\System32 in windows
    
    if sys.platform == "win32":
        path = f"C:\\windows\\System32\\{file}"
    else:
        os.system(f"chmod +x {file}")
        path = f"/usr/local/bin/{file}"
    
    # move {file} to {path}
    try:
        os.rename(file, path)
    except Exception as e:
        log.error(f"installation failed: {e}")
        
def delete(file):
    log.info(f"uninstalling {file}...")
    # check if the file exists
    if sys.platform == "win32":
        if not os.path.isfile(f"C:\\windows\\System32\\{file}"):
            log.error(f"package '{file}' not installed")
    else:
        if not os.path.isfile(f"/usr/local/bin/{file}"):
            log.error(f"package '{file}' not installed")
            
    if sys.platform == "win32":
        path = f"C:\\windows\\System32\\{file}"
    else:
        path = f"/usr/local/bin/{file}"
    os.remove(path)