
import pathlib as pl

class ProjectDirectoryDoesNotExist(Exception):

    def __init__(self, directory: pl.Path):

        self.message = f"Directory {directory} does not exist, please specify a valid project directory."

class ProjectFileDoesNotExist(Exception):

    def __init__(self, directory: pl.Path, project: str, extension: str):

        self.message = f"Project file {project}.{extension} could not be found in project {project}."

class InvalidConfig(Exception):

    def __init__(self, msg: str):

        self.message = f"Invalid config: {msg}."

class NoFilesCouldBeCreated(Exception):

    def __init__(self, files: [str]):
        
        self.message = f"No files could be created: {files}"

class UnsupportedPlatform(Exception):

    def __init__(self):
        
        self.message = "Only Linux or Windows are valid platforms."

class InvalidFileType(Exception):

    def __init__(self, specified_type):

        self.message = f"Only \"ustruct\", \"header\", \"source\" or \"build\" may be specified as generation modes (actual value: {specified_type})."