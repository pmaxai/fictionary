import random, json, os
from fictionary import FictionaryLayer

class FictionaryMap():
    def __init__(self, path="./fictionary/map"):
        self.map = {}        
        self.register = {}
        if path: self.from_folder(path)
    
    def add_mapping(self, keyword, register_no):
        self.map[keyword] = register_no
    
    
    def new_register_no(self):
        while(True):
            register_no = random.randint(1000000, 9999999)
            if register_no not in self.register:
               return str(register_no)
        
            
    
    def do(self, find, get):
        if find in self.map:
            return self.register[self.map[find]][get]
        
    
    def from_file(self, path):
        with open(path, 'r') as f:
            for line in f:
                jsonline = json.loads(line)
                self.registrate(jsonline)
                
    
    def from_folder(self, path):
        if not path.endswith("/"): path += ("/") 
        filenames = os.listdir(path)
        for file in filenames: 
            self.from_file(path + file)
    
    def get_map(self):
        return self.map
    
    def get_register(self):
        return self.register
    
    def registrate(self, mapping):
        register_no = self.new_register_no()
        self.register[register_no] = mapping
        for key in mapping["mapping"]:
            self.map[mapping[key]] = register_no
    
    def as_layer(self):
        fl = FictionaryLayer()
        tmplayer = FictionaryLayer()
        for register_no in self.register:
            mapping = self.register[register_no]
            for key in mapping:
                origin = "undefined"
                if 'origin' not in mapping:
                    if 'country' in mapping:
                        origin = mapping['country'].lower()
                elif 'origin' in mapping:
                    origin = mapping['origin']
                
                
                if key != 'mapping' and key != 'origin':                    
                    tmplayer.extend(key, origin, [mapping[key]])
            fl.fuse(tmplayer)
        return fl

