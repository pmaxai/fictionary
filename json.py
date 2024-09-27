import json

class FictionaryJson():
    def __init__(self, path=None):
        self.json = {}
        if path: self._importFromFile(path)

    def _importFromFile(self, path):
        with open(path, "r") as file:
            self.json = json.load(file)
    
    def generate(self, fictionary):
        generate_json = {}
        for key in self.json:
            split = self.json[key].split(":")
            fiction = split[0]
            origin = None
            if len(split) == 2: 
                origin = split[1]    
            generate_json[key] = fictionary.choose(fiction, origin)
        
        return generate_json
        
