import sqlite3


class AcessConstTables:
    def __init__(self, dbname="rentbot.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def get_avito_room(self, room_num):
        stmt = "SELECT avito FROM room_info WHERE room_num =(?)"
        args = (room_num,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_dom_room(self, room_num):
        stmt = "SELECT domofond FROM room_info WHERE room_num =(?)"
        args = (room_num,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_avito_metro(self, metroname):
        stmt = "SELECT metro_code FROM metro_info WHERE metro_name =(?)"
        args = (metroname,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_dom_metro(self, metroname):
        stmt = "SELECT metro_link FROM metro_info WHERE metro_name =(?)"
        args = (metroname,)
        return [x[0] for x in self.conn.execute(stmt, args)]
