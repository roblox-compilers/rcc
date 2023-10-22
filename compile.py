import os, requests, time, sys, subprocess, code
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
        saferun(name + " -v > /dev/null")
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
def saferun(cmd):
    succ = subprocess.run(cmd, shell=True)
    if succ.returncode != 0:
        log.error("operation failed")
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
        check_exec("qts")
        pkgs = []
        if os.path.exists("package.json"):
            with open("package.json", "r") as f:
                package = json.load(f)
            if "dependencies" in package:
                for i in package["dependencies"]:
                    pkgs.append(i)
        saferun("qts " + file + " -o " + refileformat(outfile, fileformat(file), "lua") + " -I " + " -I ".join(pkgs))
        return "ts"
    def compile_kt(file, outfile):
        check_exec("rbxkt")
        saferun("rbxkt " + file + " -o " + refileformat(outfile, fileformat(file), "lua"))
        return "kt"
    def compile_asm(file, outfile):
        check_exec("rasm")
        saferun("rasm " + file + " > " + refileformat(outfile, fileformat(file), "lua"))
        return "asm"
    def compile_teal(file, outfile):
        tl_link = "https://raw.githubusercontent.com/teal-language/tl/master/tl.lua"
        lib = requests.get(tl_link).text
        lib = "\n".join(lib.split("\n")[:-2])
        lib += "\nRCCTEAL = tl\n"
        lib += """RCCTEAL.pyprocess = function(file)
    res, err = tl.process(file)
    return {
        result = res,
        error = err
    }
end

RCCTEAL.write_out = function(tlconfig, result, output_file) -- from Teal CLI
   local ofd, err = io.open(output_file, 'wb')

   if not ofd then
      return {
        error = err
      }
   end

   local _
   _, err = ofd:write(tl.pretty_print_ast(result.ast, tlconfig.gen_target) .. "\\n")
   if err then
      return {
          error = err
      }
   end

   ofd:close()
   
   return {}
end

RCCTEAL.report = function(category, errors)
    if not errors then
        return false
    end
    if #errors > 0 then
        local n = #errors
        for _, err in ipairs(errors) do
        print("\\27[1;31m"..category.." \\27[0m\\27[90mTEAL rcc-teal:\\27[0m " .. err.filename .. ":\\27[1m" .. err.y .. ":" .. err.x .. ": " .. (err.msg or "") .. "\\27[0m")
        end
        return true
    end
    return false
end
RCCTEAL.reportwarn = function(category, errors)
    if not errors then
        return false
    end
    if #errors > 0 then
        local n = #errors
        for _, err in ipairs(errors) do
            print("\\27[1;33mwarning \\27[0m\\27[90mTEAL rcc-teal:\\27[0m " .. err.filename .. ":\\27[1m" .. err.y .. ":" .. err.x .. ": " .. (err.msg or "") .. "\\27[0m")
        end
        return true
    end
    return false
end
"""
        embed = """try:
    import lupa
except:
    log.error("lupa not installed, please install it using 'pip install lupa'")
lua = lupa.LuaRuntime()
def get(lib):
    lua.execute(lib)
    tl = lua.globals().RCCTEAL
    return tl"""
        embeded_globals = {}
        exec(embed, embeded_globals)
        tl = embeded_globals["get"](lib)
        compiled = tl.pyprocess(file)
        if compiled.error:
            log.error(compiled.error)
        if len(compiled.result.syntax_errors) == 0:
            if len(compiled.result.warnings) > 0:
                tl.reportwarn("warning", compiled.result.warnings)
            if len(compiled.result.type_errors) > 0:
                tl.report("type error", compiled.result.type_errors)
                sys.exit(1)
            ret = tl.write_out({
                "gen_target": "lua51"
                }, compiled.result, refileformat(outfile, fileformat(file), "lua"))
            if ret.error:
                log.error(ret.error)
        else:
            print("\n")
            tl.report("syntax error", compiled.result.syntax_errors)
            sys.exit(1)
            
        return "tl"
    def compile_yue(file, outfile):
        log.error("YueScript is not supported yet")
        #check_exec("tl")
        #saferun("tl check " + file)
        #saferun("tl gen " + file)
        return "yue"
    def compile_jupyter(file, outfile):
        check_exec("rbxpy")
        saferun("rbxpy " + file + " -r -j -o " + refileformat(outfile, fileformat(file), "lua"))
        return "py"
    
    def compile_moon(file, outfile):
        log.error("MoonScript is not supported yet")
        #check_exec("tl")
        #saferun("tl check " + file)
        #saferun("tl gen " + file)
        return "moon"
    def passthrough(file, outfile):
        shutil.copyfile(file, outfile)
        return "lua"
    
def compile(indir, outdir):
    startTime = time.time()
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
            log.info("Compiling " + file + "...")
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
    log.info("Adding runtime libraries...")
    if not os.path.exists(outdir + "/../include"):
        os.mkdir(outdir + "/../include")
    runtime.RuntimeEngine.load(languages, outdir + "/../include")
    
    log.info("Successfully compiled project in: " + str(time.time() - startTime) + " seconds")