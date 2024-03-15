import os, requests, time, sys, subprocess, code
import log
import runtime
import texteng
import json

try:
    import shutil
except:
    log.error("shutil not installed, please install it using 'pip install shutil'")
    
def check_exec(name, check = "-v"):
    format = "/dev/null"
    if os.name == "nt":
        format = "NUL"
    try:
        saferun(f"{name} {check} > {format}")
    except:
        log.error("compiler " + name + " not installed or cannot initialize")
summerize = {
    # Python
    "py": "compile_py",
    "ipynb": "compile_jupyter",
    
    # C & C++
    "c": "compile_c",
    "C": "compile_c",
    "cpp": "compile_c",
    "cxx": "compile_c",
    
    # C#
    "cs": "compile_cs",
    
    # TS
    "ts": "compile_ts",
    "tsx": "compile_ts",
    
    # Kotlin
    "kt": "compile_kt",
    
    # Assembly
    "asm": "compile_asm",
    "S": "compile_asm",
    "rasm": "compile_asm",
    
    # Lua (passthrough/check)
    "lua": "passthrough",
    "luau": "passthrough_check",
}

ts = ["ts", "tsx"]
def refileformat(file, old, new):
    return ".".join(file.split(".")[:-1]) + "." + new
def fileformat(file):
    return file.split(".")[-1]
def saferun(cmd, fallback = None):
    succ = subprocess.run(cmd, shell=True)
    if succ.returncode != 0:
        if fallback:
            fallback()
        log.error("operation failed")
def analyze(file):
    succ = subprocess.run("luau-analyze "+file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if succ.returncode != 0:
        log.error("luau stopped compilation")
class Compilers:
    def compile_py(file, outfile):
        check_exec("rbxpy")
        saferun("rbxpy " + file + " -r -o " + refileformat(outfile, fileformat(file), "lua"))
        return "py"
    def compile_c(file, outfile):
        check_exec("rbxc")
        saferun("rbxc " + file + " -o " + refileformat(outfile, fileformat(file), "lua"))
        return "c"
    def compile_cs(file, outfile):
        check_exec("rbxcs")
        saferun("rbxcs " + file + " -o " + refileformat(outfile, fileformat(file), "lua"))
        return "cs"
    def compile_ts(file, outfile):

        return "ts"
    def compile_kt(file, outfile):
        check_exec("rbxkt")
        saferun("rbxkt " + file + " -o " + refileformat(outfile, fileformat(file), "lua"))
        return "kt"
    def compile_asm(file, outfile):
        check_exec("rasm")
        saferun("rasm " + file + " > " + refileformat(outfile, fileformat(file), "lua"))
        return "asm"
    def compile_jupyter(file, outfile):
        check_exec("rbxpy")
        saferun("rbxpy " + file + " -r -j -o " + refileformat(outfile, fileformat(file), "lua"))
        return "py"
    def passthrough(file, outfile):
        shutil.copyfile(file, outfile)
        return "lua"
    def passthrough_check(file, outfile):
        check_exec("luau-analyze", "")
        analyze(file)
        shutil.copyfile(file, outfile)
        return "lua"
    
def compile(indir, outdir, predir):
    tsOn = False
    startTime = time.time()
    # check if indir exists
    if not os.path.exists(indir):
        log.error(indir+" does not exist")
    # if outdir does not exist, create it
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    else:
        # Clear outdir
        for root, dirs, files in os.walk(outdir):
            for file in files:
                os.remove(root + "/" + file)
            for dir in dirs:
                shutil.rmtree(root + "/" + dir)
                
        
    # walk through files in indir
    languages = []
    for root, dirs, files in os.walk(indir):
        for file in files:
            ext = file.split(".")[-1]
            if ext in ts:
                if not os.path.exists(indir + "/../tsconfig.json"):
                    log.error("tsconfig.json not found")
                tsOn = True
            if ext not in summerize:
                if not hasattr(texteng.TextEng, ext):
                    log.error("file extension '" + ext + "' not supported")
                else:
                    # remove head from root
                    rootitems = root.split("/")
                    rootitems[0] = outdir
                    outfile = "/".join(rootitems) + "/" + file
                    file = root + "/" + file
                    # if any of the parent folders of outfile do not exist, create them
                    if not os.path.exists("/".join(outfile.split("/")[:-1])):
                        os.makedirs("/".join(outfile.split("/")[:-1]))
                    # if the file ends with .meta.+ext, skip it and just add it to outdir
                    if file.split(".")[-2] == "meta":
                        shutil.copyfile(file, outfile)
                        continue
                    with open(file, "r") as f: 
                        code = f.read()
                    compiled = getattr(texteng.TextEng, ext)(code)
                    with open(refileformat(outfile, ext, "lua"), "w") as f:
                        f.write(compiled)
                    continue
            summerized = summerize[ext]
            compiler = getattr(Compilers, summerized)
            # remove head from root
            rootitems = root.split("/")
            rootitems[0] = outdir
            outfile = "/".join(rootitems) + "/" + file
            file = root + "/" + file
            # if any of the parent folders of outfile do not exist, create them
            if not os.path.exists("/".join(outfile.split("/")[:-1])):
                os.makedirs("/".join(outfile.split("/")[:-1]))
            # compile
            languages.append(compiler(file, outfile))
    # remove duplicates from languages
    languages = list(set(languages))
    
    # typescript
    if tsOn:
        #if os.path.exists(outdir + "/../"+predir):
        #    log.error("TS branch already exists, please delete '"+predir+"' before compiling to TS")
        #def defer():
        #    # delete outdir+/../+predir
        #   shutil.rmtree(outdir + "/../"+predir)

        #log.info("Compiling to TS...")

        #shutil.copytree(outdir + "/../", predir)

        check_exec("rbxtsc")
        saferun("rbxtsc")
        #saferun("rbxtsc -p " + outdir + "/../"+predir, defer)
        #try:
        #    predir_ext = outdir + "/../"+predir
        #    # go through files in predir/+indir
        #    tsFiles = []
        #    for root, dirs, files in os.walk(predir_ext + "/" + indir):
        #        for file in files:
        #            ext = file.split(".")[-1]
        #            if ext in ts:
        #                # add full path relative to predir_ext+indir
        #                tsFiles.append(root + "/" + file.replace(predir_ext, ""))
        #    # grab all ts files, move them to outdir out of predir
        #    for file in tsFiles:
        #        print(file)
        #        shutil.move(file, outdir + "/" + file)
        #except Exception as e:
        #    defer()
        #    log.error("failed to merge TS branch: " + str(e))
        
        #defer()
    # add runtime libraries
    #log.info("Adding runtime libraries...")
    if not os.path.exists(outdir + "/../include"):
        os.mkdir(outdir + "/../include")
    runtime.RuntimeEngine.load(languages, outdir + "/../include")
    
    log.info("Successfully compiled project in: " + str(time.time() - startTime) + " seconds")