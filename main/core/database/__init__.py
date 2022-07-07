from main.core.database.postgres.afk_sql import AFKSQL
from main.core.database.postgres.notes_sql import NOTESSQL
from main.core.database.postgres.pmpermit_sql import PMPERMITSQL
from main.core.database.postgres.dv_sql import DVSQL
from main.core.database.postgres.welcome_sql import WELCOMESQL
from main.core.database.postgres.filters_sql import FILTERSSQL




class Database(
	AFKSQL,
	NOTESSQL,
	PMPERMITSQL,
	DVSQL,
	WELCOMESQL,
	FILTERSSQL
	):
	pass
	
