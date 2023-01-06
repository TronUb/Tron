from sqlalchemy import (
    Column, 
    String, 
    Integer
)

from . import BASE, SESSION



class SUDOTABLE(BASE):
    __tablename__ = "SUDO TABLE"

    sudo_id = Column(Integer, primary_key=True)
    sudo_name = Column(String(10), default=False)
    sudo_type = Column(String(6), default="common")

    def __init__(self, sudo_id, sudo_name, sudo_type, sudo_cmds):
        self.sudo_id = sudo_id
        self.sudo_name = sudo_name
        self.sudo_type = sudo_type
        self.sudo_cmds = sudo_cmds


SUDOTABLE.__table__.create(checkfirst=True)




class SUDOSQL(object):
    def set_sudo(self, sudo_id, sudo_name, sudo_type, sudo_cmds):
        try:
            r = SESSION.query(SUDOTABLE).get(sudo_id)
            if r:
                SESSION.delete(r)
            r = SUDOTABLE(
                int(sudo_id),
                str(sudo_name),
                str(sudo_type),
                str(sudo_cmds)
            )
            SESSION.add(r)
            SESSION.commit()
        finally:
            SESSION.close()


    def get_sudo(self, sudo_id):
        try:
            return SESSION.query(SUDOTABLE).get(sudo_id)
        finally:
            SESSION.close()


    def all_sudo(self):
        try:
            ALL_SUDO = {}
            r = SESSION.query(SUDOTABLE).all()
            for x in r:
                ALL_SUDO.update(
                    {
                        x.sudo_id : {
                            "sudo_name" : x.sudo_name,
                            "sudo_type" : x.sudo_type,
                            "sudo_cmds" : eval(x.sudo_cmds)
                        }
                    }
                )
            return ALL_SUDO
        finally:
            SESSION.close()


