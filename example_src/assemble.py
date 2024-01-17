import sys
from pathlib import Path

import pandas as pd

from main import INDEX_COLS, PREDICTION_COLS, SUBMISSION_DIR

DATA_DIR = Path("/code_execution/data/")
SUBMISSION_FORMAT_PATH = DATA_DIR / "submission_format.csv"
OUTPUT_PATH = SUBMISSION_DIR / "submission.csv"


def main(chain_dir: Path) -> pd.DataFrame:
    submission_df = pd.read_csv(SUBMISSION_FORMAT_PATH, index_col=INDEX_COLS)
    for csv_path in chain_dir.glob("*.csv"):
        prediction_df = pd.read_csv(csv_path, index_col=INDEX_COLS)
        submission_df.loc[prediction_df.index] = prediction_df.loc[:, PREDICTION_COLS]
    return submission_df


if __name__ == "__main__":
    chain_dir = Path(sys.argv[1])
    chain_paths = list(sorted(chain_dir.glob("*.csv")))
    print(f"assembling all predictions for {len(chain_paths):,} chains ...")
    df = main(chain_dir)
    df.to_csv(OUTPUT_PATH, index=True)
    print(f"wrote {len(df):,} lines of output to {OUTPUT_PATH}")
