# https://datacarpentry.org/python-ecology-lesson/09-working-with-sql/index.html
# https://www.digitalocean.com/community/tutorials/how-to-use-the-sqlite3-module-in-python-3
import sqlite3

# Create a SQL connection to our SQLite database
connect = sqlite3.connect('test.db') # portal_mammals.sqlite
cursor = connect.cursor()

# Create table
cursor.execute("""CREATE TABLE faculty (fid INT, fname TEXT, qualification TEXT, deptid INTEGER);""")

# Insert data
cursor.execute("""INSERT INTO faculty VALUES (1, 'Aman', 'B.Tech', 1);""")
connect.commit()

cursor.execute("""INSERT INTO faculty VALUES (2, 'Mohan', 'M.Tech', 1), 
                                             (3, 'Vishal', 'M.Tech', 1), 
                                             (4, 'Priya', 'Ph.D', 2),
                                             (5, 'Ravi', 'Ph.D', 3),
                                             (6, 'Aarti', 'M.Tech', 2);""")
connect.commit()
