
import pathlib as pl
import os
import generate_config as cfg
import exceptions as exc


def generate_header(config: cfg.Configuration):

    # select project or plugin
    base = config.dir
    if config.use_plugin:
        base = base / config.plugin_root
    
    # append ustruct header and source paths
    headers = base / "Source" / config.module / "Public"  / config.file_root
    
    # create directories if necessary
    if not (headers.exists() and headers.is_dir()):
        headers.mkdir(parents=True)

    # create header files
    already_present = []
    for name in config.names:

        header = headers / f"{name}.h"
        
        if header.exists():
            already_present.append(name)
        else:

            with open(header, 'w', newline='\n') as header_file:

                header_file.writelines([
                    "#pragma once\n",
                    "\n",
                    "#include \"CoreMinimal.h\"\n"
                ])

    for failed_to_create in already_present:
        print(f"Could not create file {failed_to_create}: File already exists.")
    
    if len(already_present) >= len(config.names):
        raise exc.NoFilesCouldBeCreated(config.names)

def generate_source(config: cfg.Configuration):

    # select project or plugin
    base = config.dir
    if config.use_plugin:
        base = base / config.plugin_root
    
    # append ustruct header and source paths
    sources = base / "Source" / config.module / "Private"  / config.file_root
    
    # create directories if necessary
    if not (sources.exists() and sources.is_dir()):
        sources.mkdir(parents=True)

    # create header files
    already_present = []
    for name in config.names:

        source = sources / f"{name}.cpp"
        
        if source.exists():
            already_present.append(name)
        else:

            with open(source, 'w', newline='\n') as source_file:

                source_file.writelines([
                    "\n",
                    "// TODO write source code\n"
                ])

    for failed_to_create in already_present:
        print(f"Could not create file {failed_to_create}: File already exists.")
    
    if len(already_present) >= len(config.names):
        raise exc.NoFilesCouldBeCreated(config.names)