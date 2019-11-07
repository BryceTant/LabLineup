from LLDBConnect import LLDBConnect
from user import user

db = LLDBConnect()

#Returns user info (uid, firstname, lastname, email)
def getUserInfo(uid):
    (first_name, last_name, email) = db.querySingle("select first_name, last_name, email from auth_user where username = '"+uid+"';")
    return user(uid, first_name, last_name, email)

def updateUserFirstName(uid, firstname):
    exString = "update auth_user set "
    exString = exString + "first_name = '" + firstname + "'"
    exString = exString + "where username = '" + uid + "';"
    db.execute(exString)

def updateUserLastName(uid, lastname):
    exString = "update auth_user set "
    exString = exString + "last_name = '" + lastname + "'"
    exString = exString + "where username = '" + uid + "';"
    db.execute(exString)

def updateUserFirstName(uid, email):
    exString = "update auth_user set "
    exString = exString + "email = '" + email + "'"
    exString = exString + "where username = '" + uid + "';"
    db.execute(exString)


def createLab(name, description):
    exString = "insert into labs(name, description)"
    exString = exString + " values ('" + name + "', '" + description + "')"
    db.execute(exString)

db.close()
