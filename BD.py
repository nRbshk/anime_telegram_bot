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
        logger.info("START save_anime")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        try: 
            cursor.execute("INSERT INTO anime VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, idt_, name_, status_, episode_, "00:00", get_date(), get_date(), episode_, "nb"))
        except:
            return 1
        conn.commit()
        
        conn.close()

        logger.info("START save_anime")
        return 0

    def show(self, idt_, status_ = "inProgress"):
        logger.info("START show")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        
        if status_ == "All":
            cursor.execute("SELECT * FROM anime WHERE id_telegram=?", (idt_, ))
        else:
            cursor.execute("SELECT * FROM anime WHERE id_telegram=? AND status=?", (idt_, status_,))

        list_to_print = cursor.fetchall()


        conn.close()

        logger.info("END show")
        return list_to_print

    def set_time(self, idt_, name_, time_):
        logger.info("START set_time")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET time=? WHERE id_telegram=? AND name=? AND status=?", (time_, idt_, name_, "inProgress"))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        conn.commit()

        conn.close()
        logger.info("END set_time")


    def set_status(self, idt_, name_, status_):
        logger.info("START set_status")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET status=? WHERE id_telegram=? AND name=?", (status_, idt_, name_))
        cursor.execute("UPDATE anime SET notified=? WHERE id_telegram=? AND name=?", ("False", idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        conn.commit()

        conn.close()

        logger.info("END set_status")


    def set_episode(self, idt_, name_, episode_):
        logger.info("START set_episode")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET episode=? WHERE id_telegram=? AND name=?", (episode_, idt_, name_))
        cursor.execute("UPDATE anime SET notified=? WHERE id_telegram=? AND name=?", ("False", idt_, name_))
        cursor.execute("UPDATE anime SET time=? WHERE id_telegram=? AND name=?", ("00:00", idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))


        conn.commit()

        conn.close()
        logger.info("END set_episode")


    def select_notified_ep(self, link_loc_: str = "nb"):
        logger.info("START select_notified_ep")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM anime WHERE status=? AND link_loc=?", ("inProgress", link_loc_))

        response = cursor.fetchall()
        
        names = []
        idt = []
        notified_ep = []
        
        for r in response:
            names.append(r[2])
            idt.append(r[1])
            notified_ep.append(r[-2])

        conn.close()
        del response
        
        logger.info("END select_notified_ep")
        return names, idt, notified_ep
        
    def update_notified_ep(self, idt_, name_, notified_ep_, link_loc_: str ="nb"):
        logger.info("START update_notified_ep")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET notified_ep=? WHERE id_telegram=? AND name=? AND link_loc=?", (notified_ep_, idt_, name_, link_loc_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=? AND link_loc=?", (upd_time_, idt_, name_, link_loc_))

        
        conn.commit()

        conn.close()

        logger.info("END update_notified_ep")

bd = BD()