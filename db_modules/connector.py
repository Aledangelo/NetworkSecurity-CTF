import db_modules.mySql as sql

__host = '100.103.0.26'
__user = 'alessandro'
__password = 'loportoIO99'
__port = 3306
__database = 'networkSecurity'

dbSql = sql.MySql(__host, __user, __password, __database, port=__port)
dbSql.connect()
