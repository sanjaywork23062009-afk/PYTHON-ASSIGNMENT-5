# Task A2: Design the Cleaning and Normalisation

## A2.1: Cleaning Rules
* **Missing Values**:
  * *Rule*: Apply forward fill (fill with the previous valid value) for short gaps ($\le 2$ consecutive hours) in continuous sensor readings where short-term temporal continuity holds. For longer gaps or critical baseline metrics, use the rolling median to avoid skewing trends while filling missing slots.
  * *Justification*: Forward fill preserves smooth transitions in time-series data without introducing artificial jumps, while the median is robust against extreme outliers when larger gaps occur.
* **Impossible Values**:
  * *Rule*: Filter out and discard rows containing physically impossible measurements (e.g., negative PM2.5/PM10 concentrations, relative humidity outside $0-100\%$, or absolute zero/invalid temperature extremes).
  * *Justification*: Erroneous sensor calibration or transmission glitches should not corrupt analytical models with physically unfeasible numbers.
* **Duplicate Rows**:
  * *Rule*: Identify and drop exact duplicate records that share the exact same `station_id` and `timestamp`.
  * *Justification*: Duplicate ingestion cycles result in double-counting readings, skewing aggregations and inflating dataset size unnecessarily.
* **Fahrenheit Temperatures**:
  * *Rule*: Convert all temperature readings identified in Fahrenheit to Celsius using the formula: $C = (F - 32) \times \frac{5}{9}$.
  * *Justification*: Standardising all temperature data into a single metric system ($^\circ\text{C}$) ensures consistency across all stations.

---

## A2.2: Normalisation
* **Min-Max Normalisation**:
  * *Design*: Rescales the PM2.5 values into a fixed range between 0 and 1 using the formula:
    $$x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}$$
  * *Appropriateness*: Best used when the data does not follow a Gaussian (normal) distribution and you need bounded values, such as for image-based or neural network inputs where strict range limits are required.
* **Z-Score Standardisation**:
  * *Design*: Centres the PM2.5 distribution around a mean of 0 with a standard deviation of 1 using the formula:
    $$x_{std} = \frac{x - \mu}{\sigma}$$
  * *Appropriateness*: Best used when features contain outliers or follow a normal distribution, as it preserves relative variance and is ideal for distance-based machine learning algorithms (e.g., clustering or regression).

---

## A2.3: Formatting
* **Dates**: ISO 8601 standard format (`YYYY-MM-DD HH:MM:SS` in UTC).
* **Station Names**: Trimmed strings, title-cased, with standardized prefixes (e.g., `ST-001`).
* **Numbers**: Rounded to fixed decimal precision (e.g., floating-point sensor values like PM2.5, temperature, and humidity rounded to 2 decimal places).

---

## Alternative Concept and Complexity Analysis
### Impact of Dropping Missing Readings vs Imputation

* **Effect on Daily Averages**:
  * Dropping missing values reduces the sample size per day. If missingness is random (MCAR), daily averages remain relatively unbiased but have higher variance. If missingness is systematic (e.g., sensors failing during peak pollution events), dropping missing rows introduces severe survival bias, skewing daily averages downward. Imputation (forward fill/median) preserves temporal structure and prevents systematic bias under specific missing data patterns.
* **Time Complexity**:
  * *Dropping missing values*: $O(n)$ linear scan to filter out `null` entries.
  * *Forward fill*: $O(n)$ single-pass linear scan carrying forward the previous valid state.
  * *Computing a median*: $O(n \log n)$ due to the sorting requirement across values or sliding windows.
* **Space Complexity**:
  * *Dropping*: Reduces memory footprint as rows are removed from the working DataFrame.
  * *Imputation (Forward fill / Median)*: Maintains the original size $O(n)$ in memory, requiring additional space for temporary buffers during sorting or rolling window computations.
```[cite: 2]
