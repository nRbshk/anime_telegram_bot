import sqlite3

# # ANIME table
# id id_telegram name status episode time

class BD:
    def save_anime(self, idt_, name_, status_):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        # try: 
        cursor.execute("INSERT INTO anime VALUES (?, ?, ?, ?, ?, ?)", (None, idt_, name_, status_, None, None))
        # except 
        conn.commit()
        print("Anime was saved")
        conn.close()

    def show(self, idt_, status_ = "isWatching"):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM anime WHERE id_telegram=? AND status=?", (idt_, status_,))

        for val in cursor.fetchall():
            print(val)

        conn.close()

