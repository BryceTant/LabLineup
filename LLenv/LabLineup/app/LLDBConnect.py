from mysql.connector import connection

#Database settings
SET_host = '35.231.63.117'
SET_database = 'lldb'
SET_user = 'testDBUser'
SET_password = 'z5b3P9wwr9F6'
SET_autocommit = True

class LLDBConnect:
    
    #Initialize the connection
    def __init__(self):
        self.con = connection.MySQLConnection(host = SET_host, database = SET_database, user = SET_user, password = SET_password, autocommit=SET_autocommit)
        self.cursor = self.con.cursor()

    #Execute a command
    def execute(self, command):
        self.cursor.execute(command)

    #For querying multiple rows
    def query(self, command):
        self.cursor.execute(command)
        retList = []
        for output in self.cursor:
            retList.append(output)
        return retList

    #If only one row is expected
    def querySingle(self, command):
        raw = self.query(command)
        if len(raw[0]) == 1:
            return raw[0][0]
        else:
            return raw[0]
        
    #Manually commit changes
    def commit(self):
        self.con.commit()
    
    #Close the connection
    def close(self):
        self.cursor.close()
        self.con.close()
