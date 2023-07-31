import db_modules.mySql as sql

__host = '193.20.1.34'
__user = 'root'
__password = 's3cr3tp455w0rd'
__port = 3306
__database = 'vulnerable_db'

dbSql = sql.MySql(__host, __user, __password, __database, port=__port)
dbSql.connect()
