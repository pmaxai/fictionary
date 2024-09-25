import json, os, random


class Fictionary():
    def __init__(self, standard_origin="standard", load_data_on_init=True):
        self.fictionary = {}
        self.standard_origin = standard_origin
        if load_data_on_init: self._loadFromRepository()
            
    def _loadFromRepository(self):               
        filenames = os.listdir("./data")
        for path in filenames: 
            self.load("./data/"+ path)
        
    def load(self, path):
        with open(path, "r") as file:
            self.fictionary[path.split("/")[-1][:-5]] = json.load(file)
       
    def choose(self, fiction, origin=None):
        if not origin: origin = self.standard_origin
        choose_from = self.fictionary[fiction][origin]
        return choose_from[random.randint(0, len(choose_from)-1)]
    



class Template():
    def __init__(self, path=None, fictionary=None):
        self.template = []
        self.fictionary = fictionary
        if path: self._importFromFile(path)
        if not fictionary: self.fictionary = Fictionary()
        
    def _importFromFile(self, path):
        with open(path, "r") as file:
            text = file.read()
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

            self.template = result
    def generate(self):
        generation = []
        fictions = []
        json = {}
        for item in self.template:
            if item.startswith("{{") and item.endswith("}}"):
                var_split = item[2:-2].split("--")
                split = var_split[0].split(":")
                fiction = split[0]
                origin = None
                if len(split) == 2: 
                    origin = split[1]                
                generated_fiction = self.fictionary.choose(fiction, origin)
                if len(var_split) == 2:
                    json[var_split[1]] = generated_fiction                                
                fictions.append(generated_fiction)
                generation.append(generated_fiction)
                
            else:
                generation.append(item)
        return {"fictions": fictions, 
                "generation": generation,
                "json": json,
                "text": "".join(generation) }
                


class JSON():
    def __init__(self, path=None, fictionary=None):
        self.json = {}
        self.fictionary = fictionary
        if path: self._importFromFile(path)
        if not fictionary: self.fictionary = Fictionary()   

    def _importFromFile(self, path):
        with open(path, "r") as file:
            self.json = json.load(file)
    
    def generate(self):
        generate_json = {}
        for key in self.json:
            split = self.json[key].split(":")
            fiction = split[0]
            origin = None
            if len(split) == 2: 
                origin = split[1]    
            generate_json[key] = self.fictionary.choose(fiction, origin)
        
        return generate_json
        


#fn = Fictionary()
#print(fn.choose("firstname", "slavik"))
#temp = Template(path="./templates/test.txt")
#print(temp.template)
#print(temp.generate()["json"])


#json = JSON(path="./templates/testj.json")
#print(json.generate())

