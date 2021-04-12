from os import name
import sqlite3
from helpers import get_date
# # ANIME table
# id id_telegram name status episode time add_time upd_time notified
# int int text text text text text text text
available_status = ["done", "inProgress", "inList", "All"]
class BD:
    def save_anime(self, idt_, name_, status_, episode_ = 0):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        try: 
            cursor.execute("INSERT INTO anime VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, idt_, name_, status_, episode_, "00:00", get_date(), get_date(), "False"))
        except:
            return 1
        conn.commit()
        
        conn.close()
        return 0

    def show(self, idt_, status_ = "inProgress"):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        
        if status_ == "All":
            cursor.execute("SELECT * FROM anime WHERE id_telegram=?", (idt_, ))
        else:
            cursor.execute("SELECT * FROM anime WHERE id_telegram=? AND status=?", (idt_, status_,))

        list_to_print = cursor.fetchall()


        conn.close()

        return list_to_print

    def set_time(self, idt_, name_, time_):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET time=? WHERE id_telegram=? AND name=? AND status=?", (time_, idt_, name_, "inProgress"))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        conn.commit()

        conn.close()

    def set_status(self, idt_, name_, status_):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET status=? WHERE id_telegram=? AND name=?", (status_, idt_, name_))
        cursor.execute("UPDATE anime SET notified=? WHERE id_telegram=? AND name=?", ("False", idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        conn.commit()

        conn.close()

    def set_episode(self, idt_, name_, episode_):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET episode=? WHERE id_telegram=? AND name=?", (episode_, idt_, name_))
        cursor.execute("UPDATE anime SET notified=? WHERE id_telegram=? AND name=?", ("False", idt_, name_))
        cursor.execute("UPDATE anime SET time=? WHERE id_telegram=? AND name=?", ("00:00", idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))


        conn.commit()

        conn.close()


    def select_notify(self, notify: str = "False"):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM anime WHERE notified=? and status=?", (notify, "inProgress"))

        response = cursor.fetchall()
        
        names = []
        idt = []
        
        for r in response:
            names.append(r[2])
            idt.append(r[1])

        conn.close()

        del response
        
        return names, idt
        
    def update_notify(self, idt_, name_, notify: str = "True"):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()


        cursor.execute("UPDATE anime SET notified=? WHERE id_telegram=? AND name=?", (notify, idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        
        conn.commit()

        conn.close()

bd = BD()