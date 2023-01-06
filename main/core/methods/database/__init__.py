from .postgresql.afk_sql import AFKSQL
from .postgresql.notes_sql import NOTESSQL
from .postgresql.pmpermit_sql import PMPERMITSQL
from .postgresql.dv_sql import DVSQL
from .postgresql.welcome_sql import WELCOMESQL
from .postgresql.sudo_sql import SUDOSQL



class Database(
    AFKSQL,
    NOTESSQL,
    PMPERMITSQL,
    DVSQL,
    WELCOMESQL,
    SUDOSQL
    ):
    pass
    
