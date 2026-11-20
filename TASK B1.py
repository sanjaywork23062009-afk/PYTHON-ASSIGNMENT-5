import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Velachery,2026-10-04,1500
"""

def load_clean(text):
    rows = []
    reader = csv.DictReader(io.StringIO(text.strip()))
    for row in reader:
        val = row['pm25'].strip()
        if val != '' and val != 'NA':
            try:
                f_val = float(val)
                if 0 <= f_val <= 999:
                    rows.append((row['station'], row['date'], f_val))
            except ValueError:
                pass
    return rows

def min_max(values):
    if not values:
        return []
    mn = min(values)
    mx = max(values)
    if mx == mn:
        return [0.0 for _ in values]
    return [round((v - mn) / (mx - mn), 3) for v in values]

clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))
