
import pathlib as pl
import os
import generate_config as cfg
import exceptions as exc

def generate_ustructs(config: cfg.Configuration):

    # select project or plugin
    base = config.dir
    if config.use_plugin:
        base = base / config.plugin_root
    
    # append ustruct header and source paths
    headers = base / "Source" / config.module / "Public"  / config.file_root
    sources = base / "Source" / config.module / "Private" / config.file_root

    # create directories if necessary
    if not (headers.exists() and headers.is_dir()):
        headers.mkdir(parents=True)

    if not (sources.exists() and sources.is_dir()):
        sources.mkdir(parents=True)

    # create ustruct files
    already_present = []
    for ustruct in config.names:

        header = headers / f"{ustruct}.h"
        source = sources / f"{ustruct}.cpp"

        if header.exists() or source.exists():
            already_present.append(ustruct)
        else:

            with open(header, 'w', newline='\n') as header_file:

                header_file.writelines([
                    "#pragma once\n",
                    "\n",
                    "#include \"CoreMinimal.h\"\n",
                    f"#include \"{ustruct}.generated.h\"\n",
                    "\n",
                    "USTRUCT(BlueprintType)\n",
                    f"struct F{ustruct}\n",
                    "{\n",
                    "    GENERATED_BODY()\n",
                    "\n",
                    "public:\n"
                    f"    F{ustruct}();\n",
                    "\n"
                    "};\n",
                    "\n"
                ])

            with open(source, 'w', newline='\n') as source_file:
                source_file.writelines([
                    "\n",
                    f"#include \"{config.file_root}/{ustruct}.h\"\n"
                    "\n",
                    f"F{ustruct}::F{ustruct}()\n",
                    "{\n",
                    "    // UStruct initialization\n",
                    "}\n",
                    "\n"
                ])

    for failed_to_create in already_present:
        print(f"Could not create UStruct {failed_to_create}: Struct already exists.")
    
    if len(already_present) >= len(config.names):
        raise exc.NoFilesCouldBeCreated(config.names)
