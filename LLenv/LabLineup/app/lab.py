class lab:
        def __init__(self, lid, name, description):
            self.lid = lid
            self.name = name
            self.description = description
            
        def toString(self):
            return "LID:\t" + self.lid + "\tName:\t" + self.name + "\tDescription:\t" + self.description
