import sqlite3


conn = sqlite3.connect('posts.db')
curr = conn.cursor()
curr.execute()
conn.commit()
conn.close()
