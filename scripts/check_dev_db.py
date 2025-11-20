import os, sqlite3
print('dev.db exists?', os.path.exists('dev.db'))
if os.path.exists('dev.db'):
    conn = sqlite3.connect('dev.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print('tables:', cur.fetchall())
    conn.close()
else:
    print('dev.db not found')

