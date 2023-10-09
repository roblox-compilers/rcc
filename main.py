import install, log
import os
import sys

try:
    args = sys.argv[1:]
    if len(args) == 0:
        log.error("no arguments provided")
        
    if args[0] == "install":
        install.install(args[1] or log.error("package name not provided"))
    elif args[0] == "uninstall":
        install.delete(args[1] or log.error("package name not provided"))
    elif args[0] == "update":
        install.delete(args[1] or log.error("package name not provided"))
        install.install(args[1] or log.error("package name not provided"))
except:
    print()
    sys.exit(1)