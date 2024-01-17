import sys
from pathlib import Path

import cv2
import pandas as pd


SUBMISSION_DIR = Path("/code_execution/submission/")
INDEX_COLS = ["chain_id", "i"]
PREDICTION_COLS = ["x", "y", "z", "qw", "qx", "qy", "qz"]
REFERENCE_VALUES = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]


def main(sequence_dir: Path):
    chain_id = sequence_dir.name
    image_paths = list(sorted(sequence_dir.glob("*.png")))
    idxs = {int(image_path.stem): image_path for image_path in image_paths}

    # pick out the reference image
    try:
        reference_img_path = idxs[0]
        _reference_img = cv2.imread(str(reference_img_path))
    except KeyError:
        raise ValueError(f"Could not find reference image for chain {chain_id}")

    predictions = []
    for i, image_path in idxs.items():
        predictions_i = {"chain_id": chain_id, "i": i}
        if i == 0:
            values = dict(zip(PREDICTION_COLS, REFERENCE_VALUES))
        else:
            _other_image = cv2.imread(str(image_path))
            # TODO: actually make predictions! we don't actually do anything useful here!
            values = {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "qw": 0.0,
                "qx": 0.0,
                "qy": 0.0,
                "qz": 0.0,
            }
        predictions.append(predictions_i | values)

    prediction_df = pd.DataFrame.from_records(predictions)
    return prediction_df


if __name__ == "__main__":
    sequence_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    print(f"making predictions for {sequence_dir}")
    df = main(sequence_dir)
    output_path = output_dir / f"{sequence_dir.name}.csv"
    df.to_csv(output_path, index=False)
    print(f"writing predictions for {sequence_dir} to {output_path}")
