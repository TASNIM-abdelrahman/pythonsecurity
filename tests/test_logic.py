import sys
import os
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from logic import clean_data, analyze


def test_clean_data_removes_bad_rows():
    """Rows with non-numeric bytes should be dropped."""
    df = pd.DataFrame({
        "src_ip": ["10.0.0.1", "10.0.0.2"],
        "bytes": ["100", "not_a_number"],
        "status": ["ok", "ok"],
    })
    cleaned = clean_data(df)
    assert len(cleaned) == 1


def test_analyze_finds_top_talker():
    """The IP sending the most bytes should be flagged as top talker."""
    df = pd.DataFrame({
        "src_ip": ["10.0.0.1", "10.0.0.1", "10.0.0.2"],
        "bytes": [500, 500, 100],
        "status": ["ok", "ok", "ok"],
    })
    results = analyze(df)
    assert results["top_talker"] == "10.0.0.1"
    assert results["top_bytes"] == 1000