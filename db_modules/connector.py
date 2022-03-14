import db_modules.mySql as sql

__host = '192.168.1.55'
__user = 'alessandro'
__password = 'loportoIO99'
__port = 3306
__database = 'networkSecurity'

dbSql = sql.MySql(__host, __user, __password, __database, port=__port)
dbSql.connect()
