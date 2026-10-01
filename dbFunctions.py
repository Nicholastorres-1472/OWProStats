import sqlite3

URL = "Prostats.db"

def createChampionshipTable():
    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS championships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            champ_id TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,
            region TEXT NOT NULL,
            players INTEGER NOT NULL,
            start_date INTEGER NOT NULL,
            matches INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def createMatchesTable():
    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id BLOB PRIMARY KEY UNIQUE,
            region TEXT NOT NULL,
            competition_type TEXT NOT NULL,
            competition_name TEXT NOT NULL,
            team_1_name TEXT NOT NULL,
            team_1_id UUID NOT NULL,
            team_2_name TEXT NOT NULL,
            team_2_id UUID NOT NULL,
            start_time INTEGER,
            end_time INTEGER NOT NULL,
            best_of INTEGER NOT NULL,
            round INTEGER NOT NULL,
            faceit_url TEXT NOT NULL UNIQUE,
            champ_id UUID NOT NULL
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

def getChampId():

    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute("SELECT champ_id FROM championships")

    data = cursor.fetchall()

    conn.close()

    return data

def insertMatches(data):

    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()
    
    cursor.executemany(
       """INSERT OR IGNORE INTO matches (id, region, competition_type, competition_name, team_1_name, team_1_id, team_2_name, team_2_id, start_time, end_time, best_of, round, faceit_url, champ_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        data
    )
    
    conn.commit()
    conn.close()