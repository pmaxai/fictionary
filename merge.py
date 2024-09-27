
class Merge():
    def layer(original, newdata):
        for fiction in newdata:
            if fiction not in original:
                original[fiction] = {}
                
            for origin in newdata[fiction]:
                if origin not in original[fiction]:
                    original[fiction][origin] = []
           
                for keyword in newdata[fiction][origin]:
                    if keyword not in original[fiction][origin]:
                        original[fiction][origin].append(keyword)
            
        return original