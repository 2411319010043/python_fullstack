class Room:
    def __init__(self,name,owner,weight,length):
        self.name = name
        self.owner = owner
        self.__weight = weight
        self.__length = length
    
    def tell_area(self):
        return self.__weight * self.__length

r = Room('卧室','alex',10,10)

print(r.tell_area())