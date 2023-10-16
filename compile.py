import os
import log
import runtime
import texteng
import json

try:
    import shutil
except:
    log.error("shutil not installed, please install it using 'pip install shutil'")
    
def check_exec(name):
    try:
        os.system(name + " -v > /dev/null")
    except:
        log.error("compiler " + name + " not installed or cannot initialize")
summerize = {
    # Python
    "py": "compile_py",
    
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
    
    # Lua (passthrough)
    "lua": "passthrough",
    "luau": "passthrough",
    
    # Teal
    "tl": "compile_teal",
    
    # MoonScript
    "moon": "compile_moon",
    
    # YueScript
    "yue": "compile_yue",
}

def refileformat(file, old, new):
    return ".".join(file.split(".")[:-1]) + "." + new
def fileformat(file):
    return file.split(".")[-1]
class Compilers:
    def compile_py(file, outfile):
        check_exec("rbxpy")
        os.system("rbxpy " + file + " -r -o " + refileformat(outfile, fileformat(file), "lua"))
        return "py"
    def compile_c(file, outfile):
        check_exec("rbxc")
        os.system("rbxc " + file + " -o " + refileformat(outfile, fileformat(file), "lua"))
        return "c"
    def compile_cs(file, outfile):
        check_exec("rbxcs")
        os.system("rbxcs " + file + " -o " + refileformat(outfile, fileformat(file), "lua"))
        return "cs"
    def compile_ts(file, outfile):
        check_exec("qts")
        pkgs = []
        if os.path.exists("package.json"):
            with open("package.json", "r") as f:
                package = json.load(f)
            if "dependencies" in package:
                for i in package["dependencies"]:
                    pkgs.append(i)
        os.system("qts " + file + " -o " + refileformat(outfile, fileformat(file), "lua") + " -I " + " -I ".join(pkgs))
        return "ts"
    def compile_kt(file, outfile):
        check_exec("rbxkt")
        os.system("rbxkt " + file + " -o " + refileformat(outfile, fileformat(file), "lua"))
        return "kt"
    def compile_asm(file, outfile):
        check_exec("rasm")
        os.system("rasm " + file + " > " + refileformat(outfile, fileformat(file), "lua"))
        return "asm"
    def compile_teal(file, outfile):
        log.error("Teal is not supported yet")
        #check_exec("tl")
        #os.system("tl check " + file)
        #os.system("tl gen " + file)
        return "tl"
    def compile_yue(file, outfile):
        log.error("YueScript is not supported yet")
        #check_exec("tl")
        #os.system("tl check " + file)
        #os.system("tl gen " + file)
        return "yue"
    def compile_moon(file, outfile):
        log.error("MoonScript is not supported yet")
        #check_exec("tl")
        #os.system("tl check " + file)
        #os.system("tl gen " + file)
        return "moon"
    def passthrough(file, outfile):
        shutil.copyfile(file, outfile)
        return "lua"
    
def compile(indir, outdir):
    # check if indir exists
    if not os.path.exists(indir):
        log.error(indir+" does not exist")
    # if outdir does not exist, create it
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    else:
        shutil.rmtree(outdir)
        
    # walk through files in indir
    languages = []
    for root, dirs, files in os.walk(indir):
        for file in files:
            ext = file.split(".")[-1]
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
    
    # add runtime libraries
    if not os.path.exists(outdir + "/../include"):
        os.mkdir(outdir + "/../include")
    runtime.RuntimeEngine.load(languages, outdir + "/../include")