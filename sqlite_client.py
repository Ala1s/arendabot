import sqlite3


class SqLiteClient:
    def __init__(self, dbname="query_params.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS query_params (userid text, metro text," \
               " minprice INTEGER, maxprice INTEGER, rooms INTEGER )"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_user(self, user_id):
        stmt = "INSERT INTO query_params (userid) VALUES (?)"
        args = (user_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def set_metro(self, metro, user_id):
        stmt = "UPDATE query_params SET metro=(?) WHERE userid = (?) "
        args = (metro, user_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def set_minprice(self, minprice, user_id):
        stmt = "UPDATE query_params SET minprice=? WHERE userid = ? "
        args = (minprice, user_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def set_maxprice(self, maxprice, user_id):
        stmt = "UPDATE query_params SET maxprice=(?) WHERE userid = (?) "
        args = (maxprice, user_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def set_rooms(self, roomnum, user_id):
        stmt = "UPDATE query_params SET rooms=(?) WHERE userid = (?) "
        args = (roomnum, user_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_user(self, user_id):
        stmt = "DELETE FROM query_params WHERE userid =(?)"
        args = (user_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_param(self, param, user_id):
        stmt = "SELECT (?) FROM query_params WHERE userid =(?)"
        args = (param, user_id)
        return [x[0] for x in self.conn.execute(stmt, args)]
