import threading

from sqlalchemy import (
    Column, 
    UnicodeText, 
    Integer, 
    String
)

from . import SESSION, BASE




class NOTES(BASE):
    __tablename__ = "notes"

    user_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, primary_key=True)
    value = Column(UnicodeText, nullable=False)
    msgtype = Column(Integer, default=0)
    file = Column(UnicodeText)
    file_ref = Column(UnicodeText)
    message_id = Column(Integer)

    def __init__(self, user_id, name, value, msgtype, file, file_ref, message_id):
        self.user_id = user_id
        self.name = name
        self.value = value
        self.msgtype = msgtype
        self.file = file
        self.file_ref = file_ref
        self.message_id = message_id

    def __repr__(self):
        return "<Note %s>" % self.name

NOTES.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

SELF_NOTES = {}




class NOTESSQL(object):
    # save a note
    def save_selfnote(self, user_id, note_name, note_data, msgtype, file=None, file_ref=None, message_id=0):
        global SELF_NOTES
        with INSERTION_LOCK:
            prev = SESSION.query(NOTES).get((user_id, note_name))
            if prev:
                SESSION.delete(prev)
            note = NOTES(user_id, note_name, note_data, msgtype=int(msgtype), file=file, file_ref=file_ref, message_id=message_id)
            SESSION.add(note)
            SESSION.commit()
    
            if not SELF_NOTES.get(user_id):
                SELF_NOTES[user_id] = {}
            SELF_NOTES[user_id][note_name] = {'value': note_data, 'type': msgtype, 'file': file, 'file_ref': file_ref, 'message_id': message_id}


    # get a saved note
    def get_selfnote(self, user_id, note_name):
        if not SELF_NOTES.get(user_id):
            SELF_NOTES[user_id] = {}
        return SELF_NOTES[user_id].get(note_name)


    # get list of saved notes
    def get_all_selfnotes(self, user_id):
        if not SELF_NOTES.get(user_id):
            SELF_NOTES[user_id] = {}
            return None
        allnotes = list(SELF_NOTES[user_id])
        allnotes.sort()
        return allnotes


    # get all saved notes with inline buttons
    def get_all_selfnote_inline(self, user_id):
        if not SELF_NOTES.get(user_id):
            SELF_NOTES[user_id] = {}
            return None
        # Sorting
        allnotes = {}
        sortnotes = list(SELF_NOTES[user_id])
        sortnotes.sort()
        for x in sortnotes:
            allnotes[x] = SELF_NOTES[user_id][x]
        return allnotes


    # remove a saved note
    def rm_selfnote(self, user_id, note_name):
        global SELF_NOTES
        with INSERTION_LOCK:
            note = SESSION.query(NOTES).get((user_id, note_name))
            if note:
                SESSION.delete(note)
                SESSION.commit()
                SELF_NOTES[user_id].pop(note_name)
                return True
    
            else:
                SESSION.close()
                return False


    # load notes while startup
    def load_allnotes():
        global SELF_NOTES
        getall = SESSION.query(NOTES).distinct().all()
        for x in getall:
            if not SELF_NOTES.get(x.user_id):
                SELF_NOTES[x.user_id] = {}
            SELF_NOTES[x.user_id][x.name] = {'value': x.value, 'type': x.msgtype, 'file': x.file, 'file_ref': x.file_ref, 'message_id': x.message_id}




NOTESSQL.load_allnotes()
