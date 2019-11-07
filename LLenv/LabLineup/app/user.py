class user:
        def __init__(self, uid, firstname, lastname, email):
            self.uid = uid
            self.firstname = firstname
            self.lastname = lastname
            self.email = email
            
        def toString(self):
            finalString = "UID:\t" + self.uid
            finalString = finalString + "\tFirst Name:\t" + self.firstname
            finalString = finalString + "\tLast Name:\t" + self.lastname
            finalString = finalString + "\tEmail:\t" + self.email
            return finalString
