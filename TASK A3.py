# Task A3: Design the Analysis and Visualisation

## A3.1: Choose the Charts
* **The trend of PM2.5 over a month**:
  * *Chart Type*: Line Chart.
  * *Justification*: Effectively displays sequential time-series data, highlighting temporal trends, fluctuations, and peaks over continuous daily intervals.
* **Comparison of stations**:
  * *Chart Type*: Box Plot (or Bar Chart).
  * *Justification*: A box plot displays the distribution, median, interquartile range, and outliers of PM2.5 levels across multiple stations simultaneously, enabling quick comparative analysis.
* **The relationship between temperature and PM2.5**:
  * *Chart Type*: Scatter Plot.
  * *Justification*: Visualizes correlation between two continuous variables, showing clustering, trends, or potential inverse/direct relationships between ambient temperature and pollution levels.
* **The hours with the worst air**:
  * *Chart Type*: Bar Chart (or Heatmap).
  * *Justification*: Aggregates readings by hour of the day (0–23) to clearly rank and compare average pollution levels across different times, highlighting peak pollution hours.

---

## A3.2: Design the Summary Table
### Daily Summary Table Schema (Per Station)
* `station_id` (TEXT): Unique station identifier.
* `date` (DATE): The specific calendar day.
* `min_pm25` (REAL): Minimum valid PM2.5 reading for the day.
* `max_pm25` (REAL): Maximum valid PM2.5 reading for the day.
* `mean_pm25` (REAL): Average valid PM2.5 reading for the day.
* `valid_readings_count` (INTEGER): Total number of valid (non-null, non-outlier) readings recorded on that day.

### Production Mechanism
Produced using an optimized SQL aggregation query grouped by station and date:
```sql
SELECT 
    station_id,
    DATE(timestamp) AS reading_date,
    MIN(pm25) AS min_pm25,
    MAX(pm25) AS max_pm25,
    AVG(pm25) AS mean_pm25,
    COUNT(pm25) AS valid_readings_count
FROM readings
WHERE status = 'Active' AND pm25 IS NOT NULL
GROUP BY station_id, DATE(timestamp);
