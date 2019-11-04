class user:
        def __init__(self, uid, firstname, lastname, email, phoneNo):
            self.uid = uid
            self.firstname = firstname
            self.lastname = lastname
            self.email = email
            self.phoneNo = phoneNo
            
        def toString(self):
            finalString = "UID:\t" + self.uid
            finalString =+ "\tFirst Name:\t" + self.firstname
            finalString =+ "\tLast Name:\t" + self.lastname
            finalString =+ "\tEmail:\t" + self.email
            finalString =+ "\tphoneNo:\t" + self.phoneNo
            return finalString
