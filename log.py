import sys

def error(msg):
    print(f"\033[1;31merror \033[0m\033[90mCORE rcc:\033[0m {msg}")
    sys.exit(1)
    
def info(msg):
    print(f"\033[1;33minfo \033[0m\033[90mCORE rcc:\033[0m {msg}")