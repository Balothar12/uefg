
import generate_config as cfg
import subprocess as sp
import os

def update_project(config: cfg.Configuration):

    # remember cwd and cd into the project directory
    cwd = os.getcwd()
    os.chdir(config.dir)

    # generate project files
    build_script_args = [
        str(cfg.build_script(config)), "-ProjectFiles", "UsePrecompiled", "-2019", str(cfg.uproject(config)), "-Game"
    ]
    if(config.source_build):
        build_script_args.append("Engine")
    sp.call(build_script_args)

    # build the project
    sp_call = [
        str(cfg.build_script(config)), f"{config.project}Editor", "Win64", "Development", str(cfg.uproject(config))
    ]

    sp.call(sp_call)

    # go back to the previous working directory
    os.chdir(cwd)