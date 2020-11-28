
import pathlib as pl
import argparse as ap
import exceptions as exc
import sys
from enum import Enum

class GenerationMode(Enum):
    USTRUCT = 1
    HEADER = 2
    SOURCE = 3
    BUILD = 4
    UOBJECT = 5

class Configuration:

    def __init__(self):

        self.dir            = pl.Path()
        self.project        = ""
        self.use_plugin     = False
        self.plugin_root    = ""
        self.plugin_name    = ""
        self.names          = []
        self.file_root      = ""
        self.module         = ""
        self.engine_root    = ""
        self.source_build   = False
        self.uobject_parent = ""

        self.mode = GenerationMode.USTRUCT

def generate_config():

    parser = ap.ArgumentParser()

    parser.add_argument("directory",        action="store", type=str,
        help="The project directory to target.")
    parser.add_argument("--project",        action="store", type=str, required=True,    dest="project",
        help="The target project within the project directory.")
    parser.add_argument("--plugin-root",    action="store", type=str,                   dest="plugin_root",
        help="Root directory of the plugin - defaults to Plugins/<PluginName> if --plugin is used.")
    parser.add_argument("--plugin",         action="store", type=str,                   dest="plugin",
        help="Target a plugin within the specified project.")
    parser.add_argument("--names",          action="store", type=str, required=True,    dest="names",   nargs="*",
        help="List of UStruct names to generate (these are the names without the 'F' prefix).")
    parser.add_argument("--file-root",      action="store", type=str, required=True,    dest="file_root",
        help="Location of the UStruct in the source tree (i.e. below Source/<Module>/[Private, Public])")
    parser.add_argument("--module",         action="store", type=str, required=False,   dest="module",  default="",
        help="Module to add the ustruct to (path below Source: Source/<Module>/...)")

    parser.add_argument("--engine",         action="store", type=str, required=True,    dest="engine",
        help="Root folder of the engine to use")
    parser.add_argument("--prebuilt",         action="store_true",                      dest="prebuilt",
        help="Is the engine the launcher version (prebuilt) or a source build")

    parser.add_argument("--parent",         action="store", type=str,                   dest="parent",
        help="Parent class for UObjects.")

    parser.add_argument("--mode",           action="store", type=str,                   dest="mode",    default="ustruct")

    arguments = parser.parse_args()

    config = Configuration()

    # check validity (i.e. plugin_root must be specified if plugin is used)
    if hasattr(arguments, "plugin") and arguments.plugin:
        if not arguments.plugin_root:
            arguments.plugin_root = f"Plugins/{arguments.plugin}"

        config.use_plugin = True
        config.plugin_name = arguments.plugin
        config.plugin_root = arguments.plugin_root

    config.dir = pl.Path(arguments.directory)
    config.project = arguments.project
    config.names = arguments.names
    config.file_root = arguments.file_root

    if hasattr(arguments, "module") and arguments.module:
        config.module = arguments.module
    else:
        if config.use_plugin:
            config.module = config.plugin_name
        else:
            config.module = config.project

    config.engine_root = arguments.engine
    config.source_build = not arguments.prebuilt

    config.uobject_parent = arguments.parent

    # check mode
    if arguments.mode == "ustruct":
        config.mode = GenerationMode.USTRUCT
    elif arguments.mode == "header":
        config.mode = GenerationMode.HEADER
    elif arguments.mode == "source":
        config.mode = GenerationMode.SOURCE
    elif arguments.mode == "build":
        config.mode = GenerationMode.BUILD
    elif arguments.mode == "uobject":
        config.mode = GenerationMode.UOBJECT
        if(len(config.uobject_parent) == 0):
            raise exc.InvalidConfig("UObject parent may not be empty for mode \"uobject\"")
    else:
        raise exc.InvalidFileType(arguments.mode)

    return config

def engine(config: Configuration):
    return pl.Path(config.engine_root)

def scripts(config: Configuration):
    return engine(config) / "Engine" / "Build" / "BatchFiles"

def binaries(config: Configuration):
    return engine(config) / "Engine" / "Binaries"

def sh_extension():

    extension = ".sh"

    if sys.platform == "win32":
        extension = ".bat"

    return extension

def exe_extension():

    extension = ".exe"

    if not sys.platform == "win32":
        extension = ""

    return extension

def ubt_exe(config: Configuration):
    return binaries(config) / "DotNET" / f"UnrealBuildTool{exe_extension()}"

def build_script(config: Configuration):
    return scripts(config) / f"Build{sh_extension()}"

def uat(config: Configuration):
    return scripts(config) / f"RunUAT{sh_extension()}"

def uproject(config: Configuration):
    return config.dir / f"{config.project}.uproject"

def plugin(config: Configuration):
    return config.dir / config.plugin_root

def uplugin(config: Configuration):
    return plugin(config) / f"{config.plugin_name}.uplugin"

def platform_id():

    identifier = ""

    if sys.platform == "win32":
        identifier = "Win64"
    elif sys.platform == "linux":
        identifier = "Linux"
    else:
        raise exc.UnsupportedPlatform()

    return identifier
