# pylint: disable=no-member

import json
from sqlalchemy import Column, String, Integer
from . import BASE, SESSION

class SUDOTABLE(BASE):
    __tablename__ = "sudo_table"  # Avoid space in table name

    sudo_id = Column(Integer, primary_key=True)
    sudo_name = Column(String(50), nullable=False)
    sudo_cmds = Column(String, default="[]")  # Store commands as JSON string

    def __init__(self, sudo_id, sudo_name, sudo_cmds):
        self.sudo_id = sudo_id
        self.sudo_name = sudo_name
        self.sudo_cmds = json.dumps(list(sudo_cmds))  # Store as JSON


# Create the table if it doesn't exist
SUDOTABLE.__table__.create(checkfirst=True)


class SUDOSQL:
    """Sudo command management SQL class"""

    @staticmethod
    def set_sudo(sudo_id: int, sudo_name: str, sudo_cmds: set) -> None:
        """Add or update a sudo user and their allowed commands"""
        try:
            existing = SESSION.query(SUDOTABLE).get(sudo_id)
            if existing:
                SESSION.delete(existing)

            entry = SUDOTABLE(sudo_id, sudo_name, sudo_cmds)
            SESSION.add(entry)
            SESSION.commit()
        finally:
            SESSION.close()

    @staticmethod
    def get_sudo(sudo_id: int) -> dict:
        """Get sudo details for a specific user"""
        try:
            return SUDOSQL.all_sudo().get(sudo_id, {})
        finally:
            SESSION.close()

    @staticmethod
    def del_sudo(sudo_id: int) -> bool:
        """Remove a sudo user"""
        try:
            entry = SESSION.query(SUDOTABLE).get(sudo_id)
            if entry:
                SESSION.delete(entry)
                SESSION.commit()
                return True
            return False
        finally:
            SESSION.close()

    @staticmethod
    def all_sudo() -> dict:
        """Retrieve all sudo users and their command sets"""
        try:
            all_entries = {}
            rows = SESSION.query(SUDOTABLE).all()
            for entry in rows:
                try:
                    cmds = json.loads(entry.sudo_cmds)
                except Exception:
                    cmds = []
                all_entries[entry.sudo_id] = {
                    "sudo_name": entry.sudo_name,
                    "sudo_cmds": cmds,
                }
            return all_entries
        finally:
            SESSION.close()
