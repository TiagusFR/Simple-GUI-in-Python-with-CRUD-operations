import mysql.connector


class Connect:
    def __init__(self):

        self.connection = mysql.connector.connect(host='localhost',user='root',
                                                      password='Ti@França1707',
                                                    database='standard_server',)
        

#To create table if not exists

""" 
def createTable(self):
    c = self.connection.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS products (code INT PRIMARY KEY,
    name TEXT, price INT)')

    self.connection.commit()
    c.close()
"""