from tronx.database.postgres.afk_sql import AFKSQL
from tronx.database.postgres.notes_sql import NOTESSQL
from tronx.database.postgres.pmpermit_sql import PMPERMITSQL
from tronx.database.postgres.dv_sql import DVSQL
from tronx.database.postgres.welcome_sql import WELCOMESQL
from tronx.database.postgres.filters_sql import FILTERSSQL




class Database(
	AFKSQL,
	NOTESSQL,
	PMPERMITSQL,
	DVSQL,
	WELCOMESQL,
	FILTERSSQL
	):
	pass
	
