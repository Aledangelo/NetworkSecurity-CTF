import db_modules.mySql as sql

## You have to configure your db
__host = ''
__user = ''
__password = ''
__port = 
__database = ''

dbSql = sql.MySql(__host, __user, __password, __database, port=__port)
dbSql.connect()
