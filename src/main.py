
import generate_config as cfg
import check_config as verify
import generate_ustructs as gens
import generate_uobjects as geno
import generate_generic as gen_generic
import update_project as build

if __name__ == "__main__":

    # parse arguments
    config = cfg.generate_config()

    # check config
    verify.check_config(config)

    # generate files according to the mode
    if config.mode is cfg.GenerationMode.USTRUCT:
        gens.generate_ustructs(config)
    elif config.mode is cfg.GenerationMode.UOBJECT:
        geno.generate_uobjects(config)
    elif config.mode is cfg.GenerationMode.HEADER:
        gen_generic.generate_header(config)
    elif config.mode is cfg.GenerationMode.SOURCE:
        gen_generic.generate_source(config)

    # build the project
    if config.update:
        build.update_project(config)