import sqlite3
conn = sqlite3.connect('dev.db')
cur = conn.cursor()
cur.execute("SELECT id, user_id, times, enabled, created_at FROM reminders")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()

