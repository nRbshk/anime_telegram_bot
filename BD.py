from os import name
import sqlite3
from helpers import get_date

import logging

logger = logging.getLogger(__name__)
# # ANIME table
# id id_telegram name status episode time add_time upd_time notified
# int int text text text text text text text
available_status = ["done", "inProgress", "inList", "All"]
class BD:
    def save_anime(self, idt_, name_, status_, episode_ = 0):
        logger.info("INSERT INTO BD")
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
        logger.info("SHOW FROM BD")
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
        logger.info("SET TIME")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET time=? WHERE id_telegram=? AND name=? AND status=?", (time_, idt_, name_, "inProgress"))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        conn.commit()

        conn.close()

    def set_status(self, idt_, name_, status_):
        logger.info("SET STATUS")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET status=? WHERE id_telegram=? AND name=?", (status_, idt_, name_))
        cursor.execute("UPDATE anime SET notified=? WHERE id_telegram=? AND name=?", ("False", idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        conn.commit()

        conn.close()

    def set_episode(self, idt_, name_, episode_):
        logger.info("SET EPISODE")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET episode=? WHERE id_telegram=? AND name=?", (episode_, idt_, name_))
        cursor.execute("UPDATE anime SET notified=? WHERE id_telegram=? AND name=?", ("False", idt_, name_))
        cursor.execute("UPDATE anime SET time=? WHERE id_telegram=? AND name=?", ("00:00", idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))


        conn.commit()

        conn.close()


    def select_notified_ep(self):
        logger.info("SELECT notified ep")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM anime WHERE status=?", ("inProgress",))

        response = cursor.fetchall()
        
        names = []
        idt = []
        notified_ep = []
        
        for r in response:
            names.append(r[2])
            idt.append(r[1])
            notified_ep.append(r[-1])

        conn.close()
        del response
        
        return names, idt, notified_ep
        
    def update_notified_ep(self, idt_, name_, notified_ep_):
        logger.info("UPDATE notified ep")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET notified_ep=? WHERE id_telegram=? AND name=?", (notified_ep_, idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        
        conn.commit()

        conn.close()

bd = BD()