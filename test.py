import pandas as pd
import matplotlib
matplotlib.use("Agg")          # lets it save without opening a window
import matplotlib.pyplot as plt

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: file not found — {filepath}")
        return None

def clean_data(df):
    before = len(df)
    df["bytes"] = pd.to_numeric(df["bytes"], errors="coerce")
    df = df.dropna()
    after = len(df)
    dropped = before - after
    if dropped > 0:
        print(f"Warning: dropped {dropped} rows with missing or invalid data")
    return df

    
def analyze(df):
    totals = df.groupby("src_ip")["bytes"].sum()
    top_talker = totals.idxmax()
    top_bytes = int(totals.max())

    failed = df[df["status"] == "failed"]
    failed_counts = failed["src_ip"].value_counts()

    return {
        "top_talker": top_talker,
        "top_bytes": top_bytes,
        "failed_counts": failed_counts
    }
def write_report(results, output_path="data/triage_report.txt"):
    """Write the analysis findings to a readable text report."""
    with open(output_path, "w") as f:
        f.write("=== NETWORK TRIAGE REPORT ===\n\n")
        f.write(f"Top talker (most bytes sent): {results['top_talker']} "
                f"({results['top_bytes']} bytes)\n\n")
        f.write("Failed connection attempts per IP:\n")
        for ip, count in results["failed_counts"].items():
            f.write(f"  {ip}: {count} failed\n")
    print(f"Report written to {output_path}")

def make_chart(df, output_path="data/top_talkers.png"):
    """Draw a bar chart of total bytes per IP and save it as an image."""
    totals = df.groupby("src_ip")["bytes"].sum().sort_values(ascending=False)
    totals.plot(kind="bar", title="Total Bytes Sent per IP")
    plt.xlabel("Source IP")
    plt.ylabel("Total Bytes")
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Chart saved to {output_path}")


df = load_data("data/connections.csv")
df = clean_data(df)
results = analyze(df)          # store the analysis in "results"
write_report(results)          # write the text report
make_chart(df)                 # save the chart
print(results)                 # show the findings on screen too