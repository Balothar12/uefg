
import pathlib as pl
import os
import generate_config as cfg
import exceptions as exc
from  uobject_parent_map import UObjectParentMap as uobjmap

def generate_uobjects(config: cfg.Configuration):

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

    # determine prefix (same as parent's prefix, i.e. first letter of the parent)
    class_prefix = config.uobject_parent[0]

    # determine _API macro name (project/plugin name, capitalized)
    api_macro = config.project.upper()
    if(config.use_plugin):
        api_macro = config.plugin_name.upper()
    api_macro += "_API"

    # get the include from the map (if known)
    include_map = uobjmap(config.uobject_parent)
    parent_include = include_map.include

    # create ustruct files
    already_present = []
    for uobject in config.names:

        # for parent "AActor" we need some additional functions to be defined
        constructor_definition = [
            "    // Object Initialization\n"
        ]
        actor_function_declarations = []
        actor_function_definitions = []

        if(config.uobject_parent == "AActor"):
            actor_function_declarations = [
                "\n",
                "public:\n",
                "\n",
                "    virtual void Tick(float DeltaTime) override;\n",
                "\n"
                "protected:\n",
                "\n",
                "    virtual void BeginPlay() override;\n"
            ]

            actor_function_definitions = [
                "\n",
                "// Called when the game starts or when spawned\n",
                f"void {class_prefix}{uobject}::BeginPlay()\n",
                "{\n",
                "    Super::BeginPlay();\n",
                "\n",
                "}\n",
                "\n",
                "// Called every frame\n",
                f"void {class_prefix}{uobject}::Tick(const float DeltaTime)\n",
                "{\n",
                "    Super::Tick(DeltaTime);\n",
                "\n",
                "}\n"
            ]

            constructor_definition = [
                "    // Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.\n",
                "    PrimaryActorTick.bCanEverTick = true;\n",
            ]

        header = headers / f"{uobject}.h"
        source = sources / f"{uobject}.cpp"

        if header.exists() or source.exists():
            already_present.append(uobject)
        else:

            with open(header, 'w', newline='\n') as header_file:

                header_file.writelines([
                    "#pragma once\n",
                    "\n",
                    "#include \"CoreMinimal.h\"\n",
                    parent_include,
                    f"#include \"{uobject}.generated.h\"\n",
                    "\n",
                    "UCLASS()\n",
                    f"class {api_macro} {class_prefix}{uobject} : public {config.uobject_parent}\n",
                    "{\n",
                    "    GENERATED_BODY()\n",
                    "\n",
                    "public:\n"
                    f"    {class_prefix}{uobject}();\n"] 
                    + actor_function_declarations + [
                    "\n"
                    "};\n",
                    "\n"
                ])

            with open(source, 'w', newline='\n') as source_file:
                source_file.writelines([
                    "\n",
                    f"#include \"{config.file_root}/{uobject}.h\"\n"
                    "\n",
                    "// Sets default values\n",
                    f"{class_prefix}{uobject}::{class_prefix}{uobject}()\n",
                    "{\n" ]
                    + constructor_definition + [
                    "\n",
                    "}\n"]
                    + actor_function_definitions + [
                    "\n"
                ])

    for failed_to_create in already_present:
        print(f"Could not create UStruct {failed_to_create}: Struct already exists.")
    
    if len(already_present) >= len(config.names):
        raise exc.NoFilesCouldBeCreated(config.names)
