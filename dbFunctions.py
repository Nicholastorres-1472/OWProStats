import sqlite3

URL = "Prostats.db"

def createDB():
    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS championships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            champ_id TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,
            region NOT NULL,
            players NOT NULL,
            start_date NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    
    
def insertChamps(data):

    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()
    
    cursor.executemany(
       """INSERT OR IGNORE INTO championships (name, champ_id, type, region, players, start_date) VALUES (?, ?, ?, ?, ?, ?)""",
        data
    )
    
    conn.commit()
    conn.close()
   