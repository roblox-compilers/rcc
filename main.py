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