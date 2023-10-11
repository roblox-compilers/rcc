import os
import log
import runtime
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
    "py": "compile_py",
    "c": "compile_c",
    "C": "compile_c",
    "cpp": "compile_c",
    "cxx": "compile_c",
    "cs": "compile_cs",
    "ts": "compile_ts",
    "tsx": "compile_ts",
    "kt": "compile_kt",
    "wasm": "compile_wasm",
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
        os.system("qts " + file + " -o " + refileformat(outfile, fileformat(file), "lua"))
        return "ts"
    def compile_kt(file, outfile):
        check_exec("rbxkt")
        os.system("rbxkt " + file + " -o " + refileformat(outfile, fileformat(file), "lua"))
        return "kt"
    def compile_wasm(file, outfile):
        check_exec("rbxwasm")
        os.system("rbxwasm " + file + " > " + refileformat(outfile, fileformat(file), "lua"))
        return "wasm"
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
            if not ext in summerize:
                log.error("file extension " + ext + " not supported")
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