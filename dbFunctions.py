import sqlite3, os 
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("DB_URL")

# DATABASE SETUP
def createChampionshipTable():
    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS championships (
            champ_id BLOB,
            name TEXT,
            type TEXT,
            region TEXT,
            players INTEGER,
            start_date INTEGER,
            match_count INTEGER,
            PRIMARY KEY ("champ_id")
        ) WITHOUT ROWID
    ''')

    conn.commit()
    conn.close()


def createMatchesTable():
    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id BLOB,
            region TEXT,
            competition_type TEXT,
            competition_name TEXT,
            team_1_name TEXT,
            team_1_id BLOB NOT NULL,
            team_2_name TEXT,
            team_2_id BLOB NOT NULL,
            start_time INTEGER,
            end_time INTEGER,
            best_of INTEGER,
            round INTEGER,
            champ_id BLOB NOT NULL,
            PRIMARY KEY ("match_id"),
            FOREIGN KEY("champ_id") REFERENCES "championships"("champ_id") ON DELETE CASCADE
        ) WITHOUT ROWID
    ''')

    conn.commit()

    conn.close()
   
def createMapsTable():
    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maps (
            map_id INTEGER,
            match_id BLOB NOT NULL,
            round_number INTEGER NOT NULL,
            map_name TEXT,
            PRIMARY KEY ("map_id" AUTOINCREMENT),
            UNIQUE("match_id","round_number"),
	        FOREIGN KEY("match_id") REFERENCES "matches"("match_id") ON DELETE CASCADE
        )
    ''')

    conn.commit()

    conn.close()
    
def createMaps_teams_statsTable():
    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS map_teams_stats (
            map_team_id INTEGER,
            map_id INTEGER NOT NULL,
            team_id BLOB NOT NULL,
            score INTEGER NOT NULL,
            result INTEGER NOT NULL,
            avg_elims INTEGER,
            avg_deaths INTEGER,
            name TEXT,
            total_deaths INTEGER,
            total_elims INTEGER,
            UNIQUE("map_id","team_id"),
            PRIMARY KEY ("map_team_id" AUTOINCREMENT),
            FOREIGN KEY("map_id") REFERENCES "maps"("map_id") ON DELETE CASCADE
        )
    ''')
    
    conn.commit()

    conn.close()
    
def createMaps_player_statsTable():
    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS map_player_stats (
            map_player_id INTEGER,
            map_id INTEGER NOT NULL,
            team_id BLOB NOT NULL,
            player_id BLOB NOT NULL,
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
            PRIMARY KEY ("map_player_id" AUTOINCREMENT),
            FOREIGN KEY("map_id") REFERENCES "maps"("map_id") ON DELETE CASCADE
        )
    ''')
    
    conn.commit()

    conn.close()
    
def createPlayersTable():
    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()
    
    cursor.execute('''
            CREATE TABLE "players" (
                "player_id"	BLOB UNIQUE,
                "name"	TEXT,
                "mit"	INTEGER,
                "deaths"	INTEGER,
                "assists"	INTEGER,
                "elims"	INTEGER,
                "kd"	INTEGER,
                "dmg_dealt"	INTEGER,
                "healing"	INTEGER,
                "role"	TEXT,
                PRIMARY KEY("player_id")
            )
        ''')
    
    conn.commit()

    conn.close()
 
#  INSERT FUNCTIONS 
def insertChamps(data):

    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()
    
    cursor.executemany(
       """INSERT OR IGNORE INTO championships (
           name,
           champ_id,
           type,
           region,
           players,
           start_date
        ) VALUES (?, ?, ?, ?, ?, ?)""",
        data
    )
    
    conn.commit()
    conn.close()

def insertMatches(data):

    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()
    
    preInsertion = len(data)
    
    cursor.executemany(
       """INSERT OR IGNORE INTO matches (
            match_id,
            region,
            competition_type,
            competition_name,
            team_1_name,
            team_1_id,
            team_2_name,
            team_2_id,
            start_time,
            end_time,
            best_of,
            round,
            champ_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        data
    )
    
    conn.commit()
    
    postInsertion = cursor.rowcount
    missingRows = preInsertion - postInsertion
    conn.close()
    
    if(missingRows > 0):
        print(data[0][12])
        print(f"len Data: {len(data)}")
        print(f"preinsert: {preInsertion}")
        print(f"postinsertion: {postInsertion}")
        print(f"Missing rows: {missingRows}")
    
    return (missingRows)
    
    
# GET FUNCTIONS
def getChampId():
    conn = sqlite3.connect(URL)

    cursor = conn.cursor()

    cursor.execute("SELECT champ_id FROM championships")

    data = cursor.fetchall()

    conn.close()

    return data

# EXIST FUNCTIONS 

def exist(table, column, value):
    conn = sqlite3.connect(URL)
    
    cursor = conn.cursor()
    
    query = f"""
    SELECT EXISTS (
        SELECT 1
        FROM {table}
        WHERE {column} = ?
    );
    """
    
    try:
        cursor.execute(query, (value,))
        
        result = cursor.fetchone()[0]
        
        return bool(result)
    
    finally:
        conn.close