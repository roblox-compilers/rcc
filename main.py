import install, log
import os
import sys
import compile
import template
import traceback
try:
    import inquirer
    from inquirer import List
except ImportError:
    log.error("inquirer not installed, run 'pip install inquirer'")

def help():
    print("usage: \033[31;1mrcc\033[0m [command] [options]")
    print("\033[1mCommands:\033[0m")
    print("  \033[1mhelp\033[0m\t\topen this help menu")
    print("  \033[1minit\033[0m\t\tinitialize a project")
    print("  \033[1minstall\033[0m\tinstall a compiler")
    print("  \033[1muninstall\033[0m\tuninstall a compiler")
    print("  \033[1mupdate\033[0m\tupdate a compiler")
    print("\033[1mOptions:\033[0m")
    print("  \033[1m-o\033[0m\t\toutput directory (default: out)")
    print("  \033[1m<none>\033[0m\tinput directory (default: src)")
    print("  \033[1m-d\033[0m\t\tdebug mode")
    print("\033[1mExamples:\033[0m")
    print("  \033[1mrcc\033[0m \033[1minstall\033[0m roblox-py")
    print("  \033[1mrcc\033[0m \033[1muninstall\033[0m roblox-py")
    print("  \033[1mrcc\033[0m \033[1mupdate\033[0m roblox-py")
    print("  \033[1mrcc\033[0m \033[1m-o\033[0m out")
    print("  \033[1mrcc\033[0m \033[1m-o\033[0m out src")
    print("  \033[1mrcc\033[0m \033[1minclude\033[0m @roblox/roact")
def display_option_menu(options, msg):
    questions = [
        List('option',
             message=msg,
             choices=options)
    ]

    answers = inquirer.prompt(questions)
    selected_option = answers['option']
    return selected_option

def main():#try:
    args = sys.argv[1:]
    if "-d" in args:
        global DEBUG
        DEBUG = True
        args.remove("-d")
    if len(args) == 0:
        # compile src to out
        compile.compile("src", "out")
    elif args[0] == "install":
        try: 
            install.install(args[1])
        except:
            sys.exit(1)
    elif args[0] == "uninstall":
        install.delete(args[1] or log.error("package name not provided"))
    elif args[0] == "build":
        compile.compile("src", "out")
        os.system("rojo build -o out.rbxmx")
    elif args[0] == "include":
        try: 
            compile.include(args[1])
        except:
            sys.exit(1)
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

try:
    main()
except Exception as e:
    if DEBUG:
        traceback.print_exc()
    log.error(f"an error occurred, {e}")
    sys.exit(1)
