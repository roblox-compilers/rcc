import os
import log

def check_exec(name):
    try:
        os.system(name + " -v")
    except:
        log.error("compiler " + name + " not installed or is corrupted")

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
}
class Compilers:
    def compile_py(file, outfile):
        check_exec("rbxpy")
        os.execute("rbxpy " + file + " -o " + outfile)
    def compile_c(file, outfile):
        check_exec("rbxc")
        os.execute("rbxc " + file + " -o " + outfile)
    def compile_cs(file, outfile):
        check_exec("rbxcs")
        os.execute("rbxcs " + file + " -o " + outfile)
    def compile_ts(file, outfile):
        check_exec("qts")
        os.execute("qts " + file + " -o " + outfile)
    def compile_kt(file, outfile):
        check_exec("rbxkt")
        os.execute("rbxkt " + file + " -o " + outfile)
def compile(indir, outdir):
    # check if indir exists
    if not os.path.exists(indir):
        log.error(indir+" does not exist")