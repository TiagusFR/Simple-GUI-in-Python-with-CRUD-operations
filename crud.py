from database import*

class Products(object):
    
    def __init__(self, code=0, name='', price=0):
        self.info={}
        self.code=code
        self.name=name
        self.price=price
        
def createProduct(self):
    
    base = Connect()
    try:
        c = base.connection.cursor()
        
        c.execute("INSERT INTO products (code, name, price) VALUES ("+self.code+", "+self.name+", "+self.price+")")
        base.connection.commit()
        c.close()
        
        return 'Registered!'
    except:
        return 'Unable to register'

def readProducts(self, code):
    base = Connect()
    try:
        c = base.connection.cursor()
        c.execute("SELECT* FROM products= "+code+"")
        
        for line in c:
            self.code= line[0]
            self.name= line[1]
            self.price= line[2]
            
        c.close()
        
        return 'Search done!'
    except:
        return 'Failed to search product'
    
def updateProducts(self):
    
    base = Connect()
    try:
        c = base.connection.cursor()
        
        c.execute("UPDATE products SET name="+self.name+", "+self.price+" WHERE code="+self.code+"")
        
        base.connection.commit()
        c.close()
    
        return 'Updated!'
    except:
        return 'Failed to update'
    
def deleteProducts(self):
    
    base = Connect()
    try:
        c = base.connection.cursor()
        c.execute("DELETE FROM products WHERE code="+self.code+"")
    
        base.connection.commit()
        c.close()
        
        return "Deleted!"
    except:
        return 'Failed to delete'
    
