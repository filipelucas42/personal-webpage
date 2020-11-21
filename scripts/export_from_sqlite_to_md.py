import sqlite3
conn = sqlite3.connect("blog.db")
c = conn.cursor()

c.execute("select * from articles")

for row in c:
    filename = row[1].replace(' ', '-')
    f = open("./articles/" + filename + ".md", "w+")
    f.write("---\ntitle: \"{}\"\ndate: {}\ndraft: false\n---\n\n{}".format( row[1], row[2], row[3]))
    f.close() 