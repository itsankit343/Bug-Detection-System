# Bug Detection System — Python

A portfolio-ready Python project that processes system logs, detects anomalous events, identifies recurring software errors, and generates visual insights.

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib

## Project Structure

```text
bug_detection_system/
├── data/
│   └── system_logs.csv
├── src/
│   └── bug_detector.py
├── outputs/
├── requirements.txt
└── README.md
```

## How to Run

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/bug_detector.py
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/bug_detector.py
```

## What the Project Does

1. Loads system logs from CSV.
2. Cleans timestamps, numeric fields and duplicate log IDs.
3. Identifies `ERROR` and `CRITICAL` events.
4. Detects unusually high response times using a statistical threshold.
5. Combines these signals into an anomaly flag.
6. Finds recurring error types by service.
7. Generates CSV reports and Matplotlib charts.

## Outputs

The script creates:

- `detected_anomalies.csv`
- `recurring_errors.csv`
- `recurring_errors.png`
- `anomalies_by_service.png`
- `response_time_distribution.png`

## Interview Explanation

The project automates first-level log analysis. Instead of manually scanning thousands of logs, the script uses Pandas to clean and aggregate events, NumPy/statistical logic to flag unusually high response times, and Matplotlib to visualize recurring errors and anomaly patterns.

## Note

The included log data is synthetic and intended for portfolio/learning use.
