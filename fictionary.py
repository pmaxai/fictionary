import json, os, random
from .merge import Merge as merge

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
        if fiction not in self.layer: 
            self.layer[fiction] = {}
        if origin not in self.layer[fiction]:
            self.layer[fiction][origin] = []            
        self.layer[fiction][origin] += values
    
    def fuse(self, layer):
        self.layer = merge.layer(self.layer, layer.layer)
    
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
        self.fictionary = merge.layer(self.fictionary, layer.layer)
            
    def _loadFromRepository(self):               
        filenames = os.listdir(self.folder_path)
        for file in filenames: 
            self.load(self.folder_path + file)
    
    
    def load(self, path):
        with open(path, "r") as file:
            self.fictionary[path.split("/")[-1][:-5]] = json.load(file)
       
    def choose(self, fiction, origin=None):
        if origin not in self.fictionary[fiction]: origin = "global"
        if not origin: origin = self.standard_origin
        if origin == "global":
            choose_from = []
            for key in self.fictionary[fiction]:
                choose_from += self.fictionary[fiction][key]
        else:
            choose_from = self.fictionary[fiction][origin]
        return choose_from[random.randint(0, len(choose_from)-1)]
    
    def extend(self, fiction, origin, values):
        if fiction not in self.fictionary: 
            self.fictionary[fiction] = {}
        if origin not in self.fictionary[fiction]:
            self.fictionary[fiction][origin] = []
        self.fictionary[fiction][origin] += values
    
    def list_fictions(self):
        return list(self.fictionary.keys())
    
    def list_origins(self, fiction):
        return list(self.fictionary[fiction].keys())
    
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
            



#fn = Fictionary()
#fn.extend("city", "spain", ["Bilbao", "Madrid"])
#fn.add("company_name", {"IT": ["IT Sys", "GetinTouch"]})
#fn.save("./results/fict")

#print(fn.get_origins("firstname"))
#print(fn.choose("firstname", "slavik"))
#temp = FictionaryTemplate(path="./templates/test.txt")
#temp = FictionaryTemplate()
#temp.from_text("Hi, my name is {{firstname}} {{surname}}")

#print(temp.template)
#with open("./results/invoice1.html", "w") as file:
#      file.write(temp.generate()['text'])
#print(temp.generate()["text"])


#json = FictionaryJson(path="./templates/testj.json")
#print(json.generate())

