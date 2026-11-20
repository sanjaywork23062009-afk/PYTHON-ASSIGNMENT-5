# Task A4: Plan Debugging and Profiling

## A4.1: Debugging Plan
* **Print Statements**:
  * *Usage*: Quick, ad-hoc inspection of intermediate variable states, dataframe shapes, and column value distributions during initial script development (e.g., printing `df['pm25'].min()` after applying a cleaning filter).
* **Assert Statements**:
  * *Usage*: Embedded defensive checks to validate assumptions at runtime (e.g., `assert df['humidity'].between(0, 100).all(), "Invalid humidity values found"`), causing the program to fail fast if data integrity checks fail.
* **Logging Module**:
  * *Usage*: Systematic recording of program execution flow, warning events (e.g., dropping invalid rows), and error tracking with severity levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`) outputted to both the console and a log file.
* **PDB / IDE Debugger**:
  * *Usage*: Interactive debugging session to step through complex data transformation loops line-by-line, inspect local scope variables, set conditional breakpoints, and evaluate expressions dynamically when unexpected bugs occur.

---

## A4.2: Profiling Plan
* **`time.perf_counter()`**:
  * *Usage*: Used for high-precision wall-clock timing of specific code blocks or functions (e.g., measuring how long CSV ingestion versus database insertion takes).
* **`timeit` Module**:
  * *Usage*: Benchmarking small snippets or isolated data cleaning functions repeatedly to measure average execution time and identify optimal pandas vectorisation strategies.
* **`cProfile`**:
  * *Usage*: Comprehensive deterministic profiling of the entire program to generate cumulative execution time reports per function, pinpointing exact bottlenecks and slow functions across the script.

---

## Alternative Concept and Complexity Analysis
### Print Statements vs Logging Module & Debugger

* **Solution with Print Statements Only**:
  * Relying solely on `print()` results in cluttered console output, manual cleanup of code before version control commits, lack of structured severity levels, and an inability to inspect execution states interactively without restarting execution.
* **Extra Time Added**:
  * Thousands of synchronous `print()` or `logging` calls write continuously to standard output (disk/terminal buffer). I/O operations are extremely slow in Python, adding significant overhead and artificially inflating execution time compared to silent execution.
* **Switching Off Approaches**:
  * *Print Statements*: Must be manually commented out, deleted, or wrapped in verbose flags across the codebase.
  * *Logging*: Can be switched off instantly without code modification by changing the global logging threshold level to `logging.CRITICAL` or `logging.DISABLED`.
  * *Debugger / Profiler*: Inherent zero-overhead when not invoked or when profiling decorators are removed.
```[cite: 4]
