import sqlite3
import os

class Database:
    @classmethod
    def get_instance(cls):
        """Get the unique instance of this class to work with the database"""
        if not hasattr(cls,"instance"):
            cls.instance=Database()
        return cls.instance
            
    def __init__(self, name="game.db"):
        self.name=name
    
    def connect(self):
        """Make a connection to the database"""
        try:
            path=os.path.join(os.path.dirname(os.path.dirname(__file__)), self.name)
            return sqlite3.connect(path)
        except Exception as e:
            print("error")
            
    def insert(self,table,obj):
        """Create a record for the table specified"""
        if obj.get("id"):del obj["id"]
        str_names=""
        str_values=""
        for key, value in obj.items():
            str_names+=key+","
            if type(value)==type(0):str_values+=str(value)+","
            else:str_values+="'"+str(value).replace("'", "''")+"',"
        str_names=str_names[:-1]
        str_values=str_values[:-1]
        strQuery="insert into "+table+"("+str_names+") values ("+str_values+")"
        self.query(strQuery)
    
    def query(self, strQuery):
        """Make any query and return the object"""
        con = self.connect()
        cursor = con.cursor()
        queries=[]
        if not strQuery:return
        result = []
        if not strQuery.endswith(";"):strQuery=strQuery+";"
        cursor.execute(strQuery)
        if not strQuery.startswith("select"):
            con.commit()
            
        else:
            data = cursor.fetchall()
            for row in data:
                r={}
                i=0
                for column in row:
                    if type(column)==type("") or type(column)==type(0) or not column:
                        r[cursor.description[i][0]]=column
                    else:
                        r[cursor.description[i][0]]=column[0]
                    i+=1
                result.append(r)
        con.close()
        return result
    
