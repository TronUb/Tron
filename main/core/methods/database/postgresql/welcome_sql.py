import threading

from sqlalchemy import Column, String, Integer

from . import SESSION, BASE


class WELCOME(BASE):
    __tablename__ = "welcome"

    chat_id = Column(String, primary_key=True)
    file_id = Column(String)
    text = Column(String)

    def __init__(self, chat_id, file_id, text):
        self.chat_id = chat_id
        self.file_id = file_id
        self.text = text


WELCOME.__table__.create(checkfirst=True)  # pylint: disable=E1101

INSERTION_LOCK = threading.RLock()

session = SESSION()


class WELCOMESQL(object):
    """ setwelcome, getwelcome, delwelcome, get_welcome_ids """
    def set_welcome(self, chat_id, file_id, text=None):
        with INSERTION_LOCK:
            it_exists = session.query(WELCOME).get(chat_id)
            try:
                if it_exists:
                    session.delete(it_exists)
                new_data = WELCOME(chat_id, file_id, text)
                session.add(new_data)
                session.commit()
            finally:
                session.close()
        return (chat_id, file_id, text)

    def del_welcome(self, chat_id):
        with INSERTION_LOCK:
            it_exists = session.query(WELCOME).get(chat_id)
            try:
                if it_exists:
                    session.delete(it_exists)
                    session.commit()
                    session.close()
                    return True
            except Exception as e:
                session.close()
                print(e)
                return False

    def get_welcome(self, chat_id):
        it_exists = session.query(WELCOME).get(chat_id)
        rep = None
        repx = None
        if it_exists:
            rep = str(it_exists.file_id)
            repx = it_exists.text
        session.close()
        return {"file_id" : rep, "caption" : repx}

    def get_welcome_ids(self):
        chat_ids = []
        all_welcome = session.query(WELCOME).distinct().all()
        for x in all_welcome:
            if not (int(x.chat_id) in chat_ids):
                chat_ids.append(int(x.chat_id))
        session.close()
        return chat_ids
