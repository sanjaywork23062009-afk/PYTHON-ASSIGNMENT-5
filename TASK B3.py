import csv
import io
import sqlite3
import time
import cProfile
import pandas as pd
from collections import defaultdict

data = """station,timestamp,pm25
Adyar,2026-10-01 00:00:00,45.0
Adyar,2026-10-01 01:00:00,55.0
Guindy,2026-10-01 00:00:00,90.0
Guindy,2026-10-01 01:00:00,100.0
"""

def python_loops(text):
    d = defaultdict(list)
    reader = csv.DictReader(io.StringIO(text.strip()))
    for row in reader:
        station = row['station']
        day = row['timestamp'].split()[0]
        pm = float(row['pm25'])
        d[(station, day)].append(pm)
    res = {}
    for k, vals in d.items():
        res[k] = sum(vals) / len(vals)
    return res

def pandas_groupby(text):
    df = pd.read_csv(io.StringIO(text.strip()))
    df['day'] = pd.to_datetime(df['timestamp']).dt.date.astype(str)
    grouped = df.groupby(['station', 'day'])['pm25'].mean()
    return grouped.to_dict()

def sql_group(text):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE r (station TEXT, timestamp TEXT, pm25 REAL)")
    reader = csv.reader(io.StringIO(text.strip()))
    next(reader)
    con.executemany("INSERT INTO r VALUES (?, ?, ?)", reader)
    con.commit()
    cur = con.cursor()
    cur.execute("SELECT station, SUBSTR(timestamp, 1, 10), AVG(pm25) FROM r GROUP BY station, SUBSTR(timestamp, 1, 10)")
    res = {(row[0], row[1]): row[2] for row in cur.fetchall()}
    con.close()
    return res

print("Python loops:", python_loops(data))
print("Pandas:", pandas_groupby(data))
print("SQL:", sql_group(data))

def generate_data(num_stations):
    lines = ["station,timestamp,pm25"]
    for s in range(num_stations):
        s_name = f"Station_{s}"
        for h in range(8760):
            day = f"2026-{(h//24)%365 // 30 + 1:02d}-{(h//24)%30 + 1:02d}"
            lines.append(f"{s_name},{day} {h%24:02d}:00:00,45.5")
    return "\n".join(lines)

for ns in [1, 12, 120]:
    raw_data = generate_data(ns)
    
    t0 = time.perf_counter()
    python_loops(raw_data)
    t1 = time.perf_counter()
    
    t2 = time.perf_counter()
    pandas_groupby(raw_data)
    t3 = time.perf_counter()
    
    t4 = time.perf_counter()
    sql_group(raw_data)
    t5 = time.perf_counter()
    
    print(f"Stations: {ns} | Python: {t1-t0:.4f}s | Pandas: {t3-t2:.4f}s | SQL: {t5-t4:.4f}s")

cProfile.run("python_loops(generate_data(1))")
```[cite: 11]
