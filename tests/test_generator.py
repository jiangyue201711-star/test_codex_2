import json
import subprocess
import sys
from pathlib import Path

from api_synth import TaskGenerator, summarize, validate_batch
from api_synth.contamination import is_contaminated, jaccard_similarity


def test_batch_generation_and_validation():
    tasks = TaskGenerator(seed=7).generate_batch(50, min_nonstandard_ratio=0.3)
    validate_batch(tasks, min_nonstandard_ratio=0.3)
    summary = summarize(tasks)
    assert summary.total == 50
    assert summary.nonstandard_ratio >= 0.3


def test_contamination_similarity():
    a = "implement api spec with setValue and getVal"
    b = "implement api spec with setValue and getVal"
    c = "totally different instruction for image classification"
    assert jaccard_similarity(a, b) == 1.0
    assert jaccard_similarity(a, c) < 0.82
    assert is_contaminated(a, [b], threshold=0.82)
    assert not is_contaminated(c, [b], threshold=0.82)


def test_cli_output(tmp_path: Path):
    out = tmp_path / "tasks.json"
    cmd = [
        sys.executable,
        "-m",
        "api_synth.cli",
        "--count",
        "12",
        "--seed",
        "1",
        "--output",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert len(payload["tasks"]) == 12
    assert payload["summary"]["nonstandard_ratio"] >= 0.3
