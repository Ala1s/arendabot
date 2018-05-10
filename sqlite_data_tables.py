import sqlite3


class AccessTables:
    def __init__(self, dbname="rentbot.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def check_metro(self, metro):
        stmt = "SELECT metro_name FROM metro_info WHERE metro_name =(?)"
        args = (metro,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result

    def get_avito_room(self, room_num):
        stmt = "SELECT avito FROM room_info WHERE room_num =(?)"
        args = (room_num,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result

    def get_dom_room(self, room_num):
        stmt = "SELECT domofond FROM room_info WHERE room_num =(?)"
        args = (room_num,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result

    def get_avito_metro(self, metroname):
        stmt = "SELECT metro_code FROM metro_info WHERE metro_name =(?)"
        args = (metroname,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result

    def get_dom_metro(self, metroname):
        stmt = "SELECT metro_link FROM metro_info WHERE metro_name =(?)"
        args = (metroname,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result

    def get_cyan_metro(self, metroname):
        stmt = "SELECT metro_code_c FROM metro_info WHERE metro_name =(?)"
        args = (metroname,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result


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
        stmt = "UPDATE query_params SET minprice=(?) WHERE userid = (?) "
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

    def write_result(self, user_id, val):
        stmt = "INSERT INTO results (userid, result) VALUES (?,?)"
        args = (user_id, val)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_results(self, user_id):
        stmt = "SELECT result FROM results WHERE userid =(?)"
        args = (user_id,)
        tup = self.conn.execute(stmt, args).fetchall()
        results = []
        for t in tup:
            results.append(t)
        return results

    def delete_results(self, user_id):
        stmt = "DELETE FROM results WHERE userid =(?)"
        args = (user_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_user(self, user_id):
        stmt = "DELETE FROM query_params WHERE userid =(?)"
        args = (user_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_metro(self, user_id):
        stmt = "SELECT metro FROM query_params WHERE userid =(?)"
        args = (user_id,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result

    def get_minprice(self, user_id):
        stmt = "SELECT minprice FROM query_params WHERE userid =(?)"
        args = (user_id,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result

    def get_maxprice(self, user_id):
        stmt = "SELECT maxprice FROM query_params WHERE userid =(?)"
        args = (user_id,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result

    def get_rooms(self, user_id):
        stmt = "SELECT rooms FROM query_params WHERE userid =(?)"
        args = (user_id,)
        try:
            result = str(self.conn.execute(stmt, args).fetchone()[0])
        except:
            result = None
        return result
