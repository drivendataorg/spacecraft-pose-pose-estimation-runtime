import os

from pathlib import Path

import pytest

SUBMISSION_DIR = Path("/code_execution/submission/")
SUBMISSION_PATH = SUBMISSION_DIR / "submission.csv"
CHECK_SUBMISSION = os.environ.get("CHECK_SUBMISSION", "true") == "true"


@pytest.mark.skipif(not CHECK_SUBMISSION, reason="Not checking submission yet")
def test_submission_exists():
    assert SUBMISSION_PATH.exists()
