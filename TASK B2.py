import sqlite3

readings = [("Adyar", "2026-10-01", 48.0), ("Guindy", "2026-10-01", 95.0),
("Guindy", "2026-10-03", 121.0), ("Adyar", "2026-10-04", 60.0)]

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")

con.executemany("INSERT INTO aq (station, day, pm25) VALUES (?, ?, ?)", readings)
con.commit()

def station_average(name):
    cur = con.cursor()
    cur.execute("SELECT AVG(pm25) FROM aq WHERE station = ?", (name,))
    row = cur.fetchone()
    return row[0] if row and row[0] is not None else None

print(station_average("Adyar"), station_average("Guindy"))
print(station_average("Adyar' OR '1'='1"))
con.close()
```[cite: 9, 10]
