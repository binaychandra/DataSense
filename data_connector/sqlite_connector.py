import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def push_to_sqlitedb(df, db_tblname):
    # Get the database connection object
    conn = get_db_connection()
    try:
        df.to_sql(db_tblname, conn, index=False, if_exists = 'replace')
    except:
        raise Exception("Insertion Error : DB Insertion failed..")
    return None
