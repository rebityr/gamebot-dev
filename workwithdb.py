import sqlite3

class workDB:

    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)
        self.cur = self.con.cursor()
    
    def new_user(self, table, vk_id):
        self.cur.execute(f"""INSERT INTO {table}(vk_id) VALUES ({vk_id})""")
        self.con.commit()
    
    def get_all(self, table, ret='dct'):
        _ = self.cur.execute(f"""SELECT * FROM {table}""").fetchall()
        if ret == 'dct':
            dct = {}
            for i in _:
                dct[i[1]] = i
            return dct
        elif ret == 'lst':
            return _
    
    def get_where_col(self, table, col, data):
        _ = self.cur.execute(f"""SELECT * FROM {table} WHERE {col} = '{data}'""").fetchall()
        
        return _

    def get_row_users(self, vk_id):
        _ = self.cur.execute(f"""SELECT * FROM users WHERE vk_id = '{vk_id}'""").fetchall()

        return _[0]
    
    def get_row(self, table, id):
        _ = self.cur.execute(f"""SELECT * FROM {table} WHERE id = '{id}'""").fetchall()

        return _[0]
    
    def set_cell(self, table, vk_id, column, data):
        self.cur.execute(f"""UPDATE {table} SET {column} = '{data}' WHERE vk_id = {vk_id}""")
        self.con.commit()
    
    def set_cell_by_id(self, table, id, column, data):
        self.cur.execute(f"""UPDATE {table} SET {column} = '{data}' WHERE id = {id}""")
        self.con.commit()
    
    def delete_row_from_check(self, event, id):
        self.cur.execute(f"""DELETE FROM events WHERE vk_id = '{id}' AND event = '{event}'""")
        self.con.commit()
    
    def new_event(self, event, id, time):
        self.cur.execute(f"""INSERT INTO events(vk_id, event, time) VALUES ('{id}', '{event}', {time})""")
        self.con.commit()
    
    def get_row_event(self, event, id):
        _ = self.cur.execute(f"""SELECT * FROM events WHERE vk_id = {id} AND event = '{event}'""").fetchall()

        return _
    
    def get_all_event(self):
        _ = self.cur.execute(f"""SELECT * FROM events""").fetchall()

        return _
    
    def set_cell_event(self, column, data, vk_id, event):
        self.cur.execute(f"""UPDATE events SET {column} = '{data}' WHERE vk_id = {vk_id} AND event = '{event}'""")
        self.con.commit()
    