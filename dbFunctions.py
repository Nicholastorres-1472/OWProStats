import sqlite3

URL = "Prostats_test.db"

# DATABASE SETUP
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
            match_count INTEGER
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
   
def createMapsTable():
    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maps (
            map_id BLOB PRIMARY KEY UNIQUE,
            match_id TEXT NOT NULL,
            round_number INTEGER NOT NULL,
            map_name TEXT,
            UNIQUE("match_id","round_number"),
	        FOREIGN KEY("match_id") REFERENCES "matches"("id") ON DELETE CASCADE
        )
    ''')

    conn.commit()

    conn.close()
    
def createMaps_teams_statsTable():
    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maps_teams_stats (
            map_team_id INTEGER PRIMARY KEY UNIQUE,
            map_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            result INTEGER NOT NULL,
            avg_elims INTEGER,
            avg_deaths INTEGER,
            name TEXT,
            total_deaths INTEGER,
            total_elims INTEGER,
            UNIQUE("map_id","team_id"),
            FOREIGN KEY("map_id") REFERENCES "maps"("map_id") ON DELETE CASCADE
        )
    ''')
    
def createMaps_player_statsTable():
    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maps_player_stats (
            map_player_id INTEGER PRIMARY KEY UNIQUE,
            map_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            player_id TEXT NOT NULL,
            name TEXT,
            mit INTEGER,
            deaths INTEGER,
            assists INTEGER,
            elims INTEGER,
            kd INTEGER,
            dmg_dealt INTEGER,
            healing INTEGER,
            role TEXT,
            UNIQUE("map_id","player_id"),
            FOREIGN KEY("map_id") REFERENCES "maps"("map_id") ON DELETE CASCADE
        )
    ''')
   
#  INSERT FUNCTIONS 
def insertChamps(data):

    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()
    
    cursor.executemany(
       """INSERT OR IGNORE INTO championships (name, champ_id, type, region, players, start_date) VALUES (?, ?, ?, ?, ?, ?)""",
        data
    )
    
    conn.commit()
    conn.close()

def insertMatches(data):

    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()
    
    cursor.executemany(
       """INSERT OR IGNORE INTO matches (id, region, competition_type, competition_name, team_1_name, team_1_id, team_2_name, team_2_id, start_time, end_time, best_of, round, faceit_url, champ_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        data
    )
    
    conn.commit()
    conn.close()
    
    
# GET FUNCTIONS
def getChampId():

    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute("SELECT champ_id FROM championships")

    data = cursor.fetchall()

    conn.close()

    return data