import sqlite3
from config import DB_PATH
def init_db():
 c=sqlite3.connect(DB_PATH); c.execute("CREATE TABLE IF NOT EXISTS seen(address TEXT PRIMARY KEY, ts INTEGER)"); c.execute("CREATE TABLE IF NOT EXISTS alerts(address TEXT PRIMARY KEY, ts INTEGER)"); c.commit(); c.close()
def seen(a):
 c=sqlite3.connect(DB_PATH); r=c.execute("SELECT 1 FROM seen WHERE address=?",(a,)).fetchone(); c.close(); return r is not None
def mark_seen(a,t):
 c=sqlite3.connect(DB_PATH); c.execute("INSERT OR IGNORE INTO seen VALUES(?,?)",(a,t)); c.commit(); c.close()
def alerted(a):
 c=sqlite3.connect(DB_PATH); r=c.execute("SELECT 1 FROM alerts WHERE address=?",(a,)).fetchone(); c.close(); return r is not None
def mark_alert(a,t):
 c=sqlite3.connect(DB_PATH); c.execute("INSERT OR REPLACE INTO alerts VALUES(?,?)",(a,t)); c.commit(); c.close()
