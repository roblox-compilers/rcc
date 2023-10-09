import subprocess

class RuntimeEngine:
    def py_runtime():
        return subprocess.check_output(["rbxpy", "-s"])
    
    @classmethod
    def load(self, languages, outdir):
        for i in languages:
            if i == "py":
                # make new file "pyruntime.lua" in outdir and write py_runtime() to it
                print(outdir + "/pyruntime.lua")
                with open(outdir + "/pyruntime.lua", "w") as f:
                    f.write(self.py_runtime().decode("utf-8"))