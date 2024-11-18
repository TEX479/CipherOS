import os
import socket
import sys
sys.path.append(os.getcwd())
import argparse
import traceback
import colorama, websockets, math, shutil, paramiko, progressbar, time, requests
from cipher.api import CipherAPI
import cipher.exceptions as ex
import tarfile
import importlib.util
import os
import tempfile
import shutil
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion, PathCompleter, WordCompleter
from prompt_toolkit.history import InMemoryHistory

colorama.init()

def hidec():
    print("\033[?25l", end="", flush=True) #hide cursor
    
def showc():
    print("\033[?25h", end="", flush=True) #show cursor

def error(msg):
    print(colorama.Style.BRIGHT+colorama.Fore.RED+msg+colorama.Fore.RESET+colorama.Style.NORMAL)
#variables
api = CipherAPI()
version = 1

if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists("data/cache"):
    os.mkdir("data/cache")

if not os.path.exists("data/config"):
    os.mkdir("data/config")

if not os.path.exists("data/cache/packages"):
    os.mkdir("data/cache/packages")

if not os.path.exists("data/cache/packageswhl"):
    os.mkdir("data/cache/packageswhl")
#builtin functions

@api.command()
def exit(args):
    print("Closing CipherOS")
    sys.exit(0)

@api.command(alias=["cd"])
def chdir(args):
    if os.path.isdir(args[0]):
        os.chdir(args[0])
    else:
        printerror(f"Error: {args[0]} is a file")
    api.pwd = os.getcwd()
    api.updatecompletions()

@api.command()
def mkdir(args):
    if os.path.exists(args[0]):
        os.mkdir(args[0])
    else:
        printerror(f"Error: {args[0]} exists")

@api.command(alias=["cls"])
def clear(args):
    print("\033c", end="")

@api.command(alias=["pl"])
def plugins(args):
    if args[0] == "reloadall":
        print("Reloading all plugins")
        for i in list(api.plugins):
            api.disable_plugin(api.plugins[i])
        for i in os.listdir(os.path.join(api.starterdir,"plugins")):
            api.load_plugin(os.path.join(api.starterdir,"plugins",i), api)
        print("Reload complete")
    
    elif args[0] == "disable":
        api.disable_plugin(args[1])
    
    elif args[0] == "enable":
        pass
    
    elif args[0] == "list":
        pass
    
    elif args[0] == "info":
        pass

@api.command(alias=["list","l"])
def ls(args):
    import os
    import colorama
    if len(args) > 0:
        path = args[0]
    else:
        path = api.pwd
    try:
        raw = os.listdir(path)
    except FileNotFoundError:
        printerror(f"Error: The directory '{path}' does not exist.")
        return
    except PermissionError:
        printerror(f"Error: Permission denied to access '{path}'.")
        return
    files = []
    folders = []
    for item in raw:
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path):
            files.append(item)
        elif os.path.isdir(full_path):
            folders.append(item)
    folders.sort()
    files.sort()
    for i in folders:
        print(f"{colorama.Fore.BLUE}{i}/ {colorama.Fore.RESET}")
    for i in files:
        print(f"{colorama.Fore.GREEN}{i} {colorama.Fore.RESET}")

@api.command()
def touch(args):
    if not os.path.exists(args[0]):
        open(args[0],"w")
        print("Created file",args[0])
        api.updatecompletions()
    else:
        print(colorama.Style.BRIGHT+colorama.Fore.RED+f"Error:",args[0],"exists"+colorama.Fore.RESET+colorama.Style.NORMAL)

@api.command(alias=["rm"])
def remove(args):
    try:
        os.remove(os.path.join(api.starterdir,args[0]))
    except PermissionError:
        printerror(f"Error: Permission to delete '{args[0]}' denied")
    except FileNotFoundError:
        printerror(f"Error: '{args[0]}' does not exist.")

print("Starting CipherOS...")
if not os.path.exists("plugins"):
    os.mkdir("plugins")

if not len(os.listdir(os.path.join(api.starterdir,"plugins"))) == 0:
    for i in os.listdir(os.path.join(api.starterdir,"plugins")):
        try:
            api.load_plugin(os.path.join(api.starterdir,"plugins",i),api)
        except:
            printerror(f"Error: Plugin '{i}' failed to load\n")
else:
    print("No plugins found")

print(colorama.Fore.MAGENTA+"Made by @mas6y6, @malachi196, and @overo3 (on github)")

print(r"""   _______       __              ____  _____
  / ____(_)___  / /_  ___  _____/ __ \/ ___/
 / /   / / __ \/ __ \/ _ \/ ___/ / / /\__ \ 
/ /___/ / /_/ / / / /  __/ /  / /_/ /___/ / 
\____/_/ .___/_/ /_/\___/_/   \____//____/  
      /_/                                   

Project Codename: Paradox"""+colorama.Fore.RESET)

history = InMemoryHistory()
command_completer = WordCompleter(api.completions, ignore_case=True)
api.updatecompletions()

while True:
    try:
        # Construct command line info
        if api.addressconnected == "":
            commandlineinfo = f"{api.currentenvironment} {api.pwd}"
        else:
            commandlineinfo = f"{api.currentenvironment} {api.addressconnected} {api.pwd}"

        # Use prompt_toolkit to gather input
        user_input = prompt(f"{commandlineinfo}> ",completer=command_completer ,history=history)

        # Split input into arguments
        _argx = user_input.split(" ")

        if not _argx[0] == "":
            cmd = _argx[0]
            e = api.run(_argx)
            
            # Command output handling
            if e[0] == 404:
                printerror(f"Error: Command \"{cmd}\" not found")
            elif not e[0] == 0:
                printerror(f"Error: Command \"{cmd}\" encountered an error\n{e[1]}")
            else:
                pass
        else:
            pass
    except (EOFError, KeyboardInterrupt):
        print()
        exit(None)
        break
