import mysql.connector


class MySql():
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306) -> None:
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port = port
        self.__database = database

    def connect(self) -> None:  
        self.__conn = mysql.connector.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            port=self.__port,
            database=self.__database
        )

    
    def selectRowByParam(self, paramKey: str, paramValue: str, table: str) -> list:
        query = f"SELECT * FROM {table} WHERE  {paramKey} = '{paramValue}';"
        
        try:
            c = self.__conn.cursor(prepared=True)
            c.execute(query)
            rows = c.fetchall()  
            result = []
            for r in rows:  
                result.append(dict(zip(c.column_names, r)))
        except ConnectionError as e:
            result = []
        except mysql.connector.errors.InterfaceError as e:
            result = []
            
        return result

    def updateRowByParam(self, paramKey1: str, paramValue: str, table: str, paramKey2: str, Value: str):
        query = f"UPDATE {table} SET {paramKey1} = '{Value}' WHERE  {paramKey2} = '{paramValue}';"
        c = self.__conn.cursor(prepared=True)
        c.execute(query)
        self.__conn.commit()

    def insertAccount(self, paramValue1: str, paramValue2: str, paramValue3: str,
                  paramValue4: str, paramValue5: str, paramValue6: str, paramValue7: str, paramValue8: str):
        try:
            query = f"INSERT INTO greenaccount(nome,cognome,citta,email,pwd,cellulare,nascita,valid) VALUES " \
                    f"('{paramValue1}','{paramValue2}','{paramValue3}','{paramValue4}','{paramValue5}','{paramValue6}','" \
                    f"{paramValue7}','{paramValue8}');"
            c = self.__conn.cursor(prepared=True)
            c.execute(query)
            self.__conn.commit()
            return True
        except Exception:
            return False

    def deleteSession(self, paramValue: str, table: str):
        query = f"UPDATE {table} SET sessione = null WHERE id = {paramValue}"
        c = self.__conn.cursor(prepared=True)
        c.execute(query)
        self.__conn.commit()

    def deleteRowByParam(self, paramKey: str, paramValue: str, table: str):
        query = f"DELETE FROM {table} WHERE {paramKey} = '{paramValue}';"
        c = self.__conn.cursor(prepared=True)
        c.execute(query)
        self.__conn.commit()

    def insertToken(self, paramValue1: str, paramValue2: str, paramValue3: str, table: str):
        query = f"INSERT INTO {table}(id,token,userType) VALUES ('{paramValue1}','{paramValue2}','{paramValue3}');"
        c = self.__conn.cursor(prepared=True)
        c.execute(query)
        self.__conn.commit()


if __name__ == '__main__':
    host='database-1.cpmyqifdjztx.us-east-1.rds.amazonaws.com'
    user='admin'
    password='3dun9d840fwedec-ceosdcsi'
    port=3306
    database='green'

    table = 'session'
    paramKey = 'token'
    paramValue = '12'

    db = MySql(host, user, password, database, port)
    db.connect()
    r = db.insertAccount('giovanni','esposito','virginia' ,'ciao@ciao.com', 'ciao', '1234567', '10/10/10', str(123456))

# db = MySql(host, user, password, port, database)
# db.connect()
# r = db.selectRowByParam(paramKey, paramValue, table)
# print(r)
