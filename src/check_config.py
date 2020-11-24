
import glob
import pathlib as pl
import exceptions as exc
import os
import generate_config as cfg

# call from within the project directory
def check_config(config : cfg.Configuration):
    
    # make sure that the project path exists
    if not config.dir.exists():
        raise exc.ProjectDirectoryDoesNotExist(config.dir)

    # make sure that the project solution and uproject files exist
    if not (config.dir / f"{config.project}.sln").exists():
        raise exc.ProjectFileDoesNotExist(config.dir, config.project, "sln")

    if not (config.dir / f"{config.project}.uproject").exists():
        raise exc.ProjectFileDoesNotExist(config.dir, config.project, "uproject")

    if config.use_plugin:

        # check plugin directory and file if a plugin is the target
        if not (config.dir / config.plugin_root / f"{config.plugin_name}.uplugin").exists():
            raise exc.ProjectFileDoesNotExist(config.dir / config.plugin_root, config.plugin_name, "uplugin")
