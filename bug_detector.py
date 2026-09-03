"""
Bug Detection System
Processes system logs with Pandas/NumPy and identifies anomalies/recurring errors.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "system_logs.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_and_clean():
    df = pd.read_csv(DATA_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["response_time_ms"] = pd.to_numeric(df["response_time_ms"], errors="coerce")
    df = df.dropna(subset=["timestamp", "level", "service", "error_type"])
    df = df.drop_duplicates(subset=["log_id"])
    return df


def detect_anomalies(df):
    df = df.copy()

    # Statistical anomaly rule: response times above mean + 2 standard deviations.
    mean_rt = df["response_time_ms"].mean()
    std_rt = df["response_time_ms"].std()

    threshold = mean_rt + 2 * std_rt
    df["response_time_anomaly"] = df["response_time_ms"] > threshold

    # Error/critical events are treated as software-error candidates.
    df["error_event"] = df["level"].isin(["ERROR", "CRITICAL"])

    # Final anomaly flag.
    df["anomaly"] = df["response_time_anomaly"] | df["error_event"]

    return df, threshold


def save_reports(df, threshold):
    anomaly_df = df[df["anomaly"]].copy()
    anomaly_df.to_csv(OUTPUT_DIR / "detected_anomalies.csv", index=False)

    recurring = (
        df[df["error_event"]]
        .groupby(["service", "error_type"])
        .size()
        .reset_index(name="occurrences")
        .sort_values("occurrences", ascending=False)
    )
    recurring.to_csv(OUTPUT_DIR / "recurring_errors.csv", index=False)

    print(f"Response-time anomaly threshold: {threshold:.2f} ms")
    print(f"Total logs: {len(df)}")
    print(f"Detected anomalies: {int(df['anomaly'].sum())}")
    print("\nTop recurring errors:")
    print(recurring.head(10).to_string(index=False))


def create_visuals(df):
    # Error counts by type
    error_counts = df[df["error_event"]]["error_type"].value_counts()
    error_counts.plot(kind="bar")
    plt.title("Recurring Software Errors")
    plt.xlabel("Error Type")
    plt.ylabel("Occurrences")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "recurring_errors.png", dpi=150)
    plt.close()

    # Anomalies by service
    anomaly_service = df[df["anomaly"]]["service"].value_counts()
    anomaly_service.plot(kind="bar")
    plt.title("Detected Anomalies by Service")
    plt.xlabel("Service")
    plt.ylabel("Anomalies")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "anomalies_by_service.png", dpi=150)
    plt.close()

    # Response time distribution
    plt.hist(df["response_time_ms"], bins=30)
    plt.title("Response Time Distribution")
    plt.xlabel("Response Time (ms)")
    plt.ylabel("Log Count")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "response_time_distribution.png", dpi=150)
    plt.close()


def main():
    df = load_and_clean()
    df, threshold = detect_anomalies(df)
    save_reports(df, threshold)
    create_visuals(df)
    print(f"\nReports and charts saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
