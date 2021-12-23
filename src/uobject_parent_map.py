
class UObjectParentMap:

    def __init__(self, parent, additional_includes = None):

        self.map = {
            "AActor": "#include \"GameFramework/Actor.h\"\n",
            "UObject": "#include \"UObject/Object.h\"\n",
            "UUserWidget": "#include \"Blueprint/UserWidget.h\"\n",
        }

        if additional_includes:
            for uobj, include in additional_includes.items():
                self.map[uobj] = include

        if parent not in self.map:
            self.include = ""
        else:
            self.include = self.map[parent]