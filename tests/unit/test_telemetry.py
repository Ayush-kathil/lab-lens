import os
import csv
import pytest
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / "scripts"))
from telemetry import MemoryTelemetry

def test_telemetry_initialization(tmp_path):
    run_dir = tmp_path / "test_run"
    telem = MemoryTelemetry(run_dir)
    assert run_dir.exists()
    assert telem.csv_path.exists()
    assert telem.peak_rss == 0

def test_event_recording_and_csv(tmp_path):
    run_dir = tmp_path / "test_run"
    telem = MemoryTelemetry(run_dir)
    telem.record("test_event", epoch=1, batch=10)
    
    with open(telem.csv_path, 'r') as f:
        reader = list(csv.reader(f))
        assert len(reader) == 2  # header + 1 row
        assert reader[0] == ["timestamp", "event", "epoch", "batch", "process_rss_mb", "system_available_mb", "system_used_mb", "system_percent"]
        assert reader[1][1] == "test_event"
        assert reader[1][2] == "1"
        assert reader[1][3] == "10"

def test_peak_memory_tracking(tmp_path):
    run_dir = tmp_path / "test_run"
    telem = MemoryTelemetry(run_dir)
    telem.record("event1")
    peak1 = telem.peak_rss
    assert peak1 > 0
    telem.record("event2")
    assert telem.peak_rss >= peak1

def test_graceful_behavior_no_optional_args(tmp_path):
    run_dir = tmp_path / "test_run"
    telem = MemoryTelemetry(run_dir)
    # Shouldn't crash if epoch/batch not provided
    telem.record("bare_event")
    with open(telem.csv_path, 'r') as f:
        reader = list(csv.reader(f))
        assert reader[1][1] == "bare_event"
        assert reader[1][2] == ""
        assert reader[1][3] == ""
