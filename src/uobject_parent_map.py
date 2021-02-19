
class UObjectParentMap:

    def __init__(self, parent):

        self.map = {
            "AActor": "#include \"GameFramework/Actor.h\"\n",
            "UObject": "#include \"UObject/Object.h\"\n",
            "UUserWidget": "#include \"Blueprint/UserWidget.h\"\n",
        }

        if parent not in self.map:
            self.include = ""
        else:
            self.include = self.map[parent]