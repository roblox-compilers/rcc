import subprocess

class RuntimeEngine:
    def py_runtime():
        return subprocess.check_output(["rbxpy", "-s"])
    def c_runtime():
        return subprocess.check_output(["rbxc", "-s"])
    @classmethod
    def load(self, languages, outdir):
        for i in languages:
            if i == "py":
                # make new file "pyruntime.lua" in outdir and write py_runtime() to it
                with open(outdir + "/pyruntime.lua", "w") as f:
                    f.write(self.py_runtime().decode("utf-8"))
            elif i == "c":
                # make new file "pyruntime.lua" in outdir and write py_runtime() to it
                with open(outdir + "/cruntime.lua", "w") as f:
                    f.write(self.c_runtime().decode("utf-8"))
                