
import argparse as ap
import os
import glob
import sys
import pathlib as pl
import json
import subprocess as sp

parser = ap.ArgumentParser()

parser.add_argument("mode", 
    help="select the mode: either \"ustruct\", \"uobject\", \"header\", \"source\" or \"build\".")
parser.add_argument("file_target", default="", nargs="?",
    help="This is the location in the source tree where the generated files will reside.")
parser.add_argument("--names", default=None, nargs="+", 
    help="List of names to generate. Will be UStruct/UObject names if mode == \"ustruct\" or \"uobject\", otherwise filenames.")
parser.add_argument("--parent", default="", 
    help="UObject parent class, must be the C++ class name.")

parser.add_argument("--plugin", 
    help="Optional plugin (assumed to be in <directory>/Plugins) to target instead of the default project.")

args = parser.parse_args()

# parse .uefg to get the engine root (it's a json file)
cfg_file = pl.Path(os.getcwd()) / ".uefg"
if not cfg_file.exists():
    raise Exception("Please create a .cfg JSON-file that contains the engine-root in an \"engine\"-entry")

if not args.names and args.mode != "build":
    raise Exception(f"Only \"build\" mode allows no file names to be specified (actual mode: {args.mode})")

engine = None
prebuilt = True
with open(str(cfg_file), 'r') as json_file:
    config = json.load(json_file)
    engine = config["engine"]
    prebuilt = config["prebuilt"]

# find the project in the current directory
solutions = glob.glob("*.sln")
if len(solutions) != 1:
    raise Exception(f"Not a valid UE4 Project directory ({len(solutions)} .sln files found instead of 1).")

parts = solutions[0].split(".")
project_name = ""
for idx in range(0, len(parts) - 1):
    project_name += parts[idx] + "."
project_name = project_name[:-1]

# get the python executable
py = sys.executable

# get path to main.py relative to this script
main = str(pl.Path(os.path.dirname(sys.argv[0])) / "src" / "main.py")

# construct call to main tool
call = [ py, main, os.getcwd(), "--project", project_name, "--file-root", args.file_target, "--engine", engine, "--mode", args.mode, "--parent", args.parent, "--names" ]
if args.names:
    call.extend(args.names)
else:
    call.extend([""])

if args.plugin:
    call.extend([ "--plugin", args.plugin ])

sp.call(call)
