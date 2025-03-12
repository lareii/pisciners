from utils.log import log

from tinydb import TinyDB, Query


class Database:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)
        log(0, "Database initialized.")

    def insert_data(self, table, data):
        return self.db.table(table).insert(data)

    def insert_multiple(self, table, data_list):
        return self.db.table(table).insert_multiple(data_list)

    def get_all(self, table):
        return self.db.table(table).all()

    def find(self, table, query):
        q = Query()
        return self.db.table(table).search(q.fragment(query))

    def update(self, table, query, new_data):
        q = Query()
        return self.db.table(table).update(new_data, q.fragment(query))

    def delete(self, table, query):
        q = Query()
        return self.db.table(table).remove(q.fragment(query))

    # def __del__(self):
    #     log(0, "Database closing...")
    #     self.db.close()
