import json


class Leader:
    
    leader = {
        "name": "",
        "result": int
    }

    leaders_list = list()
    
    def __init__(self, leaders_list):
        self.leaders_list = leaders_list
        
    def add_to_list(self, name, res):
        if len(self.leaders_list) > 0:
            if int(res) > int(self.leaders_list[len(self.leaders_list)-1]["result"]) and len(self.leaders_list) > 0:
                self.leader["name"] = name
                self.leader["result"] = res
                self.leaders_list.append(self.leader)
        else:
            self.leader["name"] = name
            self.leader["result"] = res
            self.leaders_list.append(self.leader)
        with open("data_file.json", "w") as write_file:
            json.dump(self.leaders_list, write_file)
            return self.leaders_list
        

 
     


    
