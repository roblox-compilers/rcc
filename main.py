import install, log
import os
import sys

args = sys.argv[1:]
if len(args) == 0:
    log.error("no arguments provided")
if args[0] == "install":
    install.install(args[1] or log.error("package name not provided"))
elif args[0] == "uninstall":
    error("uninstall not implemented")
elif args[0] == "update":
    error("update not implemented")