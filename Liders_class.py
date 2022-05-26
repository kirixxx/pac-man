import json
class Players():
    
    lider = {
        "name": "",
        "rezult": int
    }

    liders_list = list()
    
    def __init__(self,liders_list):
        self.liders_list = liders_list
        
    def add_to_list(self, name, rez):
        if  len(self.liders_list) > 0:
            if int(rez) > int(self.liders_list[len(self.liders_list)-1]["rezult"]) and len(self.liders_list) > 0:
                self.lider["name"] = name
                self.lider["rezult"] = rez
                self.liders_list.append(self.lider)
        else:
                self.lider["name"] = name
                self.lider["rezult"] = rez
                self.liders_list.append(self.lider)
        with open("data_file.json", "w") as write_file:
              json.dump(self.liders_list, write_file)
              return self.liders_list
        

 
     


    
