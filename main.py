import install, log
import os
import sys
import compile
import template
try:
    import inquirer
    from inquirer import List
except ImportError:
    log.error("inquirer not installed, run 'pip install inquirer'")

def help():
    print("usage: \033[31;1mrcc\0330m [command] [options]")
    print("\033[1mCommands:\033[0m")
    print("  \033[31;1mhelp\033[0m\t\topen this help menu")
    print("  \033[31;1minit\033[0m\t\tinitialize a project")
    print("  \033[31;1minstall\033[0m\tinstall a compiler")
    print("  \033[31;1muninstall\033[0m\tuninstall a compiler")
    print("  \033[31;1mupdate\033[0m\tupdate a compiler")
    print("\033[1mOptions:\033[0m")
    print("  \033[31;1m-o\033[0m\t\toutput directory (default: out)")
    print("  \033[31;1m<none>\033[0m\tinput directory (default: src)")
def display_option_menu(options, msg):
    questions = [
        List('option',
             message=msg,
             choices=options)
    ]

    answers = inquirer.prompt(questions)
    selected_option = answers['option']
    return selected_option

try:
    args = sys.argv[1:]
    if len(args) == 0:
        # compile src to out
        compile.compile("src", "out")
    elif args[0] == "install":
        install.install(args[1] or log.error("package name not provided"))
    elif args[0] == "uninstall":
        install.delete(args[1] or log.error("package name not provided"))
    elif args[0] == "update":
        install.delete(args[1] or log.error("package name not provided"))
        install.install(args[1])
    elif args[0] == "help":
        help()
    elif args[0] == "init":
        options = ["roblox-py", "roblox-c (C)", "roblox-c (C++)", "roblox-cs", "roblox-kt"]
        chosen = None
        if len(args) > 1:
            chosen = args[1]
        else:
            chosen = display_option_menu(options, "Select a compiler")
        template.load(chosen)
    else:
        # argparse
        # read args
        args = sys.argv[1:]
        flags = []
        inputf = None
        outputf = None

        lookForOutput = False

        for arg in args:
            if arg == "-o":
                lookForOutput = True
            elif arg.startswith("-"):
                flags.append(arg)
            elif inputf is None:
                inputf = arg
            elif lookForOutput:
                outputf = arg
                lookForOutput = False
            else:
                log.error("too many arguments")
                sys.exit(1)
                
        if inputf is None:
            log.error("no input directory provided")
            sys.exit(1)
        if outputf is None:
            log.error("no output directory provided")
            sys.exit(1)
        if not os.path.exists(inputf):
            log.error("input directory does not exist")
            sys.exit(1)
            
        compile.compile(inputf, outputf)       
except Exception as e:
    print()
    sys.exit(1)