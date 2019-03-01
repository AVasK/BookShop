# Added for the sake of OO model completeness (complexity too...)


class Man:

    def __init__(self, name, surname, contact):
        if name is None:
            self.name = ''
        else:
            self.name = str(name)
            
        self.surname = str(surname)
        self.contact = contact

    def __hash__(self):
        return hash(self.surname) ^ hash(self.name) ^ hash(self.contact)
        
    def __eq__(self, other):
        return self.surname == other.surname and\
               self.name == other.name and\
               self.contact == other.contact
        
    def __str__(self):
        return f"{self.name}{self.surname}"
        
    def __repr__(self):
        return str(self)
    
    