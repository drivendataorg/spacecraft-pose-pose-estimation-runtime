from pathlib import Path

import click
import cv2
import numpy as np
import pandas as pd
from loguru import logger

SUBMISSION_FORMAT_PATH = "/code_execution/data/submission_format.csv"
INDEX_COLS = ["chain_id", "i"]
SUBMISSION_FORMAT_DF = pd.read_csv(SUBMISSION_FORMAT_PATH, index_col=INDEX_COLS)
PREDICTION_COLS = SUBMISSION_FORMAT_DF.columns
REFERENCE_VALUES = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]


def predict_chain(chain_dir: Path):
    logger.debug(f"making predictions for {chain_dir}")
    chain_id = chain_dir.name
    image_paths = list(sorted(chain_dir.glob("*.png")))
    path_per_idx = {int(image_path.stem): image_path for image_path in image_paths}
    idxs = list(sorted(path_per_idx.keys()))

    assert idxs[0] == 0, f"First index for chain {chain_id} is not 0"
    assert (np.diff(idxs) == 1).all(), f"Skipped image indexes found in chain {chain_id}"

    # pick out the reference image
    try:
        reference_img_path = path_per_idx[0]
        _reference_img = cv2.imread(str(reference_img_path))
    except KeyError:
        raise ValueError(f"Could not find reference image for chain {chain_id}")

    # create an empty dataframe to populate with values
    chain_df = pd.DataFrame(index=pd.Index(idxs, name="i"), columns=PREDICTION_COLS)

    # make a prediction for each image
    for i, image_path in path_per_idx.items():
        if i == 0:
            predicted_values = REFERENCE_VALUES
        else:
            _other_image = cv2.imread(str(image_path))
            # TODO: actually make predictions! we don't actually do anything useful here!
            predicted_values = np.random.rand(len(PREDICTION_COLS))
        chain_df.loc[i] = predicted_values

    # double check we made predictions for each image
    assert chain_df.notnull().all(axis="rows").all(), f"Found NaN values for chain {chain_id}"

    return chain_df


@click.command()
@click.argument(
    "data_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.argument(
    "output_path",
    type=click.Path(exists=False),
)
def main(data_dir, output_path):
    data_dir = Path(data_dir).resolve()
    output_path = Path(output_path).resolve()
    assert output_path.parent.exists(), f"Expected output directory {output_path.parent} does not exist"

    logger.info(f"using data dir: {data_dir}")
    assert data_dir.exists(), f"Data directory does not exist: {data_dir}"

    # copy over the submission format so we can overwrite placeholders with predictions
    submission_df = SUBMISSION_FORMAT_DF.copy()

    image_dir = data_dir / "images"
    chain_ids = SUBMISSION_FORMAT_DF.index.get_level_values(0).unique()
    for chain_id in chain_ids:
        chain_dir = image_dir / chain_id
        assert chain_dir.exists(), f"Chain directory does not exist: {chain_dir}"
        chain_df = predict_chain(chain_dir)
        submission_df.loc[chain_id] = chain_df.values

    submission_df.to_csv(output_path, index=True)


if __name__ == "__main__":
    main()
