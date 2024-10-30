import psycopg2

conn = psycopg2.connect(database="engagement", host="localhost", user="username", password="password", port="5432")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS student1(id serial PRIMARY KEY,name varchar(50));''')

cur.execute('''INSERT INTO student1(id, name) VALUES (101,'aaa');''')

conn.commit()

cur.close()
conn.close()


