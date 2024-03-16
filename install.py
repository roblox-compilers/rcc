"""
Handles all the packages
"""
import os, sys, stat
import log
import importlib.util
try:
    import requests
except:
    log.error("requests not installed, please install it using 'pip install requests'")
import subprocess, compile, shutil
try:
    # run pyinstaller --version if that fails then error
    result = subprocess.run(["pyinstaller", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise
except:
    log.info("installing pyinstaller...")
    try:
        subprocess.call((f"{sys.executable} -m pip install pyinstaller"), shell=True, stdout=subprocess.DEVNULL, stderr=sys.stderr)
    except:
        log.error("Failed to install pyinstaller automatically. See above for error.")


def qts():
    if input("\033[1;33mreccomendation \033[0m\033[90mCORE rcc:\033[0m would you like to install qts alongside rbxts? (y/n)  ").lower() == "y":
        install("qts")
    else:
        return True
def silent(code):
    subprocess.call(code, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)    
def installrbxts():
    print("\033[1;33minfo \033[0m\033[90mCORE rcc:\033[0m rbxts requires npm to be installed")
    os.system("npm install -g typescript")
    os.system("npm install -g roblox-ts")
    
def installincludes():
    log.info("installing roblox-c includes...")
    contents = requests.get("https://raw.githubusercontent.com/roblox-compilers/roblox-c/main/src/rbx.h").text
    if sys.platform == "win32":
        with open(input("Please enter the path to your C and C++ include folder: ") + "\\rbx.h", "w") as f:
            f.write(contents)   
    else:
        with open("/usr/local/include/rbx.h", "w") as f:
            f.write(contents)
def get_input_with_default(prompt, default_value):
    response = input(prompt + f" (default: {default_value})")
    if response == '':
        return default_value
    else:
        return response

def installpyincludes():
    try:
        log.info("installing roblox-py includes...")
        from distutils.sysconfig import get_python_lib; guessedPath = (get_python_lib())
        dir = get_input_with_default("Please enter the path to your Python include folder: ", guessedPath)
        
        path = dir + "/rbx.py"
        log.info("loading binding engine...")
        contents = requests.get("https://raw.githubusercontent.com/roblox-compilers/bindings/main/fetch.py").text
        with open("roblox_bindings.py", "w") as f:
            f.write(contents)
        log.info("preparing binding engine...")
        spec = importlib.util.spec_from_file_location('roblox_bindings', 'roblox_bindings.py')
        fetch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fetch)
        log.info("generating bindings...")
        newCreator = fetch.Python()
        rendered = fetch.render(newCreator)
        log.info(f"installing bindings to {path}...")
        with open(path, "w") as f:
            f.write(rendered)
        log.info("installed bindings")
        # delete fetch
        os.remove("roblox_bindings.py")
        del rendered 
        del fetch
        del newCreator
    except Exception as e:
        log.warn(f"binding installation failed: {e}")
    
def tl():
    log.error("Teal does not need to be installed since it is prebuilt into RCC.")
    
def notact():
    log.error("not available")
    
exec = {
    "roblox-py": {
        "repo": "roblox-compilers/roblox-py",
        "darwin": "rbxpy",
        "win32": "rbxpy.exe",
        "mainfile": "src/rbxpy.py",
        "special": installpyincludes
    },
    "roblox-c": {
        "repo": "roblox-compilers/roblox-c",
        "darwin": "rbxc",
        "win32": "rbxc.exe",
        "mainfile": "src/rbxc.py",
        "special": installincludes
    }, 
    "roblox-cs": {
        "repo": "roblox-compilers/roblox-cs",
        "darwin": "rbxcs",
        "win32": "rbxcs.exe",
        "mainfile": None,
        "special": None
    },
    "roblox-ts": {
        "repo": "roblox-compilers/roblox-ts",
        "darwin": "rbxtsc",
        "win32": "rbxtsc.exe",
        "mainfile": None,
        "special": None,
        "specialin": installrbxts
    },
    "roblox-kt": {
        "repo": "roblox-compilers/roblox-kt",
        "darwin": "rbxkt",
        "win32": "rbxkt.exe",
        "mainfile": None,
        "special": notact
    },
    "qts": {
        "repo": "roblox-compilers/qts",
        "darwin": "qts",
        "win32": "qts.exe",
        "mainfile": "qts.py",
        "special": None
    },
    "roblox-asm": {
        "repo": "roblox-compilers/rasm",
        "darwin": "rasm",
        "win32": "rasm.exe",
        "mainfile": None,
        "special": None
    },
    "rcc": {
        "repo": "roblox-compilers/rcc",
        "darwin": "rcc",
        "win32": "rcc.exe",
        "mainfile": "rcc.py",
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
    "rbxasm": "roblox-asm",
    
    # Other
    "qts": "qts",
    "asm": "roblox-asm",
    "rasm": "roblox-asm",
    "rcc": "rcc",
    "tl": "teal",
    "teal": "teal",
    "moon": "moonscript",
    "ms": "moonscript",
    "yue": "yuescript",
    "ys": "yuescript",
    
    # roblox-
    "roblox-py": "roblox-py",
    "roblox-c": "roblox-c",
    "roblox-cs": "roblox-cs",
    "roblox-ts": "roblox-ts",
    "roblox-kt": "roblox-kt",
    "roblox-asm": "roblox-asm",
    "roblox-moon": "moonscript",
    "roblox-yue": "yuescript",
    "roblox-teal": "teal",
}

def installpre(pkg):
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
        sys.exit(1)   
def installloc(pkg):
    if (pkg in relative):
        if exec[relative[pkg]]["mainfile"] == None:
            installpre(pkg)
            return
        if exec[relative[pkg]]["special"]:
            exec[relative[pkg]]["special"]()
        if "specialin" in exec[relative[pkg]]:
            exec[relative[pkg]]["specialin"]()
        else:
            try:
                path = f"https://github.com/{exec[relative[pkg]]['repo']}"
                compile.check_exec("git", "--version")
                log.info(f"downloading {pkg}...")
                silent(f"git clone {path}")
                os.chdir(relative[pkg])
                log.info(f"building {pkg}...")
                os.system(f"pyinstaller {exec[relative[pkg]]['mainfile']} --onefile")
                os.chdir("dist")
                for i in os.listdir():
                    bin(i)
                os.chdir("..")
                os.chdir("..")
                def remove_readonly(func, path, exc_info, max_attempts=3):
                    if isinstance(exc_info[1], PermissionError):
                        if remove_readonly.attempts >= max_attempts:
                            raise exc_info[1]  # Rethrow the original exception
                        try:
                            os.chmod(path, stat.S_IWRITE) # Attempt to remove read-only
                        except:
                            raise exc_info[1] # Not caused by read-only
                        remove_readonly.attempts += 1
                        func(path)
                        remove_readonly.attempts = 0  # Reset the counter if successful
                    else:
                        raise exc_info[1]
                
                remove_readonly.attempts = 0  
                shutil.rmtree(relative[pkg],onerror=remove_readonly)
            except KeyboardInterrupt:
                log.error(f"installation failed: user cancelled. {exec[relative[pkg]]['repo']} may no longer be installed or may be corrupted")
def install(pkg):
    installloc(pkg)
def bin(file, lib=None):
    # Move the file to /usr/bin in macOS and Linux, and to C:\win32dows\System32 in windows
    if sys.platform != "win32":
        os.system(f"chmod +x {file}")
        log.info("secured " + file + "...")

    name = file.split(".")[len(file.split(".")) - 2]
    path = input("Please enter the path to your bin folder: ")
    try:
        shutil.move(file, path)
        if lib:
            shutil.move(lib, path)
    except Exception as e:
        log.error(f"failed to move {file}: {e}")
    log.info("successfully generated " + "bin/" + name)
        
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
