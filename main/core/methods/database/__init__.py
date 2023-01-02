from main.core.database.postgresql.afk_sql import AFKSQL
from main.core.database.postgresql.notes_sql import NOTESSQL
from main.core.database.postgresql.pmpermit_sql import PMPERMITSQL
from main.core.database.postgresql.dv_sql import DVSQL
from main.core.database.postgresql.welcome_sql import WELCOMESQL




class Database(
    AFKSQL,
    NOTESSQL,
    PMPERMITSQL,
    DVSQL,
    WELCOMESQL
    ):
    pass
    
