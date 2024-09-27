

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
                