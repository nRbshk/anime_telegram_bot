import sqlite3

# # ANIME table
# id id_telegram name status episode time
available_status = ["done", "inProgress", "inList", "All"]
class BD:
    def save_anime(self, idt_, name_, status_, episode_ = 0):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        try: 
            cursor.execute("INSERT INTO anime VALUES (?, ?, ?, ?, ?, ?)", (None, idt_, name_, status_, episode_, "00:00"))
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

        cursor.execute("UPDATE anime SET time=? WHERE id_telegram=? AND name=?", (time_, idt_, name_,))
        conn.commit()

        conn.close()

    def set_status(self, idt_, name_, status_):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE anime SET status=? WHERE id_telegram=? AND name=?", (status_, idt_, name_))

        conn.commit()

        conn.close()


bd = BD()