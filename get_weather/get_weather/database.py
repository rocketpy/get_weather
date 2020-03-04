import sqlite3


conn = sqlite3.connect('posts.db')
curr = conn.cursor()
curr.execute("""INSERT INTO """)
conn.commit()
conn.close()
