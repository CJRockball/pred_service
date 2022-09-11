import sqlite3
import pathlib
""" This file is used to set up database """

def setup_db(path):
    """ Function to create database and add tables """
    # Connect to db
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    # Create a table
    cur.execute("""DROP TABLE IF EXISTS new_data_table""")
        
    cur.execute(
        """CREATE TABLE IF NOT EXISTS new_data_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bill_prediction REAL,
                    tip REAL,
                    sex TEXT,
                    smoker TEXT,
                    day TEXT,
                    time TEXT,
                    g_size INT);"""
    )

    # Write changes
    conn.commit()
    conn.close()
    
    return

if __name__ == "__main__":
ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "new_tips.db"

print('>>>> setup_db start')
setup_db(DB_PATH)
print('>>>> setup_db complete')