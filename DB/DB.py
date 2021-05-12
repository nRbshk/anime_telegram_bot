from os import name
import sqlite3
from Helpers.helpers import get_date
from enum import Enum, unique
import logging

logger = logging.getLogger(__name__)

@unique
class DB_positions(Enum):
    id_position = 0
    id_telegram_position = 1
    name_position = 2
    status_position = 3
    episode_position = 4
    time_position = 5
    add_time_position = 6
    upd_time_position = 7
    notified_ep_position = 8
    link_loc_position = 9
    dub_or_sub_position = 10



available_status = ["done", "inProgress", "inList", "All"]
available_link_locs = ["nb", "sv"]
available_dub_sub = ['dub', 'sub']
class DB:
    def save_anime(self, idt_, name_, status_, episode_ = 0, dub_or_sub_ = "sub", nb_or_sv="nb"):
        logger.info("START save_anime")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM anime WHERE id_telegram=? AND name=?", (idt_, name_,))
        list_to_check = cursor.fetchall()
        for l in list_to_check:
            idt = l[DB_positions.id_telegram_position.value]
            name = l[DB_positions.name_position.value]
            if idt == idt_ and name == name_:
                logger.error(f"USER {idt_} and anime {name_} is existsing in bd.")
                del list_to_check
                conn.close()
                return 2
        del list_to_check
        try: 
            cursor.execute("INSERT INTO anime VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, idt_, name_, status_, episode_, "00:00", get_date(), get_date(), episode_, nb_or_sv, dub_or_sub_))
        except:
            logger.error("ERROR")
            conn.close()
            return 1
        conn.commit()
        
        conn.close()

        logger.info("END save_anime")
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

        logger.info("END set_time")
        conn.close()


    def set_status(self, idt_, name_, status_):
        logger.info("START set_status")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET status=? WHERE id_telegram=? AND name=?", (status_, idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        conn.commit()

        logger.info("END set_status")
        conn.close()



    def set_episode(self, idt_, name_, episode_):
        logger.info("START set_episode")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET episode=? WHERE id_telegram=? AND name=?", (episode_, idt_, name_))
        cursor.execute("UPDATE anime SET time=? WHERE id_telegram=? AND name=?", ("00:00", idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))


        conn.commit()

        logger.info("END set_episode")
        conn.close()

    def set_link_loc(self, idt_, name_, link_loc_):
        logger.info("START set_link_loc")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET link_loc=? WHERE id_telegram=? AND name=?", (link_loc_, idt_, name_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=?", (upd_time_, idt_, name_))

        conn.commit()

        logger.info("END set_link_loc")
        conn.close()



    def select_notified_ep(self, link_loc_: str = "nb"):
        logger.info("START select_notified_ep")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM anime WHERE status=? AND link_loc=?", ("inProgress", link_loc_))

        response = cursor.fetchall()
        
        names = []
        idt = []
        notified_ep = []
        dub_or_sub = []
        for r in response:
            names.append(r[DB_positions.name_position.value])
            idt.append(r[DB_positions.id_telegram_position.value])
            notified_ep.append(r[DB_positions.notified_ep_position.value])
            dub_or_sub.append(r[DB_positions.dub_or_sub_position.value])

        conn.close()
        del response
        
        logger.info("END select_notified_ep")
        return names, idt, notified_ep, dub_or_sub
        
    def update_notified_ep(self, idt_, name_, notified_ep_, link_loc_: str ="nb"):
        logger.info("START update_notified_ep")
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        upd_time_ = get_date()

        cursor.execute("UPDATE anime SET notified_ep=? WHERE id_telegram=? AND name=? AND link_loc=?", (notified_ep_, idt_, name_, link_loc_))
        cursor.execute("UPDATE anime SET upd_time=? WHERE id_telegram=? AND name=? AND link_loc=?", (upd_time_, idt_, name_, link_loc_))

        
        conn.commit()

        logger.info("END update_notified_ep")
        conn.close()

db = DB()