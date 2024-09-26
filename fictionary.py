import json, os, random

class FictionaryLayer():
    def __init__(self, path=None):
        self.layer = {}
        if path: self.load(path)            
    
    def add(self, fiction_name, fiction_json):
        self.layer[fiction_name] = fiction_json
    
    def add_from_file(self, path):
        with open(path, "r") as file:
            self.layer[path.split("/")[-1][:-5]] = json.load(file)

    def extend(self, fiction, origin, values):
        self.layer[fiction][origin] += values
    
    def fuse(self, layer):
        self.layer.update(layer)
    
    def load(self, path):
        with open(path, "r") as file:
            self.layer[path.split("/")[-1][:-5]] = json.load(file)
        
    def save(self, path):
        if not path.endswith("/"): path += ("/")        
        with open(path, "w") as file:
              file.write(json.dumps(self.layer))

class Fictionary():
    def __init__(self, standard_origin="global", load_data_on_init=True, path="./fictionary/data"):
        self.folder_path = path
        if not self.folder_path.endswith("/"): self.folder_path += ("/") 
        self.fictionary = {}
        self.standard_origin = standard_origin
        if load_data_on_init: self._loadFromRepository()
    
    def add(self, fiction_name, fiction_json):
        self.fictionary[fiction_name] = fiction_json
    
    def fuse(self, layer:FictionaryLayer):
        self.fictionary.update(layer.layer)
            
    def _loadFromRepository(self):               
        filenames = os.listdir(self.folder_path)
        for file in filenames: 
            self.load(self.folder_path + file)
    
    
    def load(self, path):
        with open(path, "r") as file:
            self.fictionary[path.split("/")[-1][:-5]] = json.load(file)
       
    def choose(self, fiction, origin=None):
        
        if not origin: origin = self.standard_origin
        if origin == "global":
            choose_from = []
            for key in self.fictionary[fiction]:
                choose_from += self.fictionary[fiction][key]
        else:
            choose_from = self.fictionary[fiction][origin]
        return choose_from[random.randint(0, len(choose_from)-1)]
    
    def extend(self, fiction, origin, values):
        self.fictionary[fiction][origin] += values
        
    def get_origins(self, fiction):
        origins = []
        for key in self.fictionary[fiction]:
            origins.append(key)
        return origins
    
    def generate(self, element):
        if type(element) is FictionaryJson:
            return element.generate(self)
        elif type(element) is FictionaryTemplate:
            return element.generate(self)
        elif type(element) is str:
            template = FictionaryTemplate()
            template.from_text(element)
            return template.generate(self)           



    def save(self, path):
        if not path.endswith("/"): path += ("/") 
        for key in self.fictionary:
            with open(path + key + ".json", "w") as file:
                  file.write(json.dumps(self.fictionary[key]))
            



class FictionaryTemplate():
    def __init__(self, path=None):
        self.template = []
        if path: self.from_file(path)
    
        
    def _split(self, text):
        result = []
        current_part = ""
        i = 0
        while i < len(text):
          if text[i:i+2] == "{{":
            if current_part:
              result.append(current_part)
            current_part = "{{"
            i += 2 
          elif text[i:i+2] == "}}":
            current_part += "}}"
            result.append(current_part)
            current_part = ""
            i += 2
          else:
            current_part += text[i]
            i += 1
      
        if current_part:
          result.append(current_part)
        
        return result
        
    def from_file(self, path):
        with open(path, "r") as file:
            text = file.read()           
            self.template = self._split(text)
    
    def from_text(self, text):
        self.template = self._split(text)
        
            
    def generate(self, fictionary):
        generation = []

        json = {}
        for item in self.template:
            if item.startswith("{{") and item.endswith("}}"):
                var_split = item[2:-2].split("--")
                split = var_split[0].split(":")
                fiction = split[0]
                origin = None
                if len(split) == 2: 
                    origin = split[1]                
                generated_fiction = fictionary.choose(fiction, origin)
                if len(var_split) == 2:
                    json[var_split[1]] = generated_fiction                                

                generation.append(generated_fiction)
                
            else:
                generation.append(item)

        return {"json": json,
                "text": "".join(generation) }
                
 

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
