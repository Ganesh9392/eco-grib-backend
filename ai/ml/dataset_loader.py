"""
dataset_loader.py

Responsible only for loading the training dataset.

Responsibilities
----------------
- Locate dataset
- Validate file existence
- Read Excel file
- Return Pandas DataFrame

Author: Eco-Grid AI Module
"""

from pathlib import Path
import logging

import pandas as pd


logger = logging.getLogger(__name__)


class DatasetLoader:
    """
    Loads the Eco-Grid training dataset.
    """

    def __init__(self, dataset_path: str | Path) -> None:
        self.dataset_path = Path(dataset_path)

    def load(self) -> pd.DataFrame:
        """
        Load dataset from Excel file.

        Returns
        -------
        pd.DataFrame

        Raises
        ------
        FileNotFoundError
            If dataset file does not exist.

        ValueError
            If dataset is empty.

        RuntimeError
            If dataset cannot be read.
        """

        logger.info("Loading dataset from %s", self.dataset_path)

        if not self.dataset_path.exists():
            logger.error("Dataset not found.")
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        try:
            dataframe = pd.read_excel(self.dataset_path)

        except Exception as exc:
            logger.exception("Unable to read dataset.")
            raise RuntimeError(
                "Failed to load dataset."
            ) from exc

        if dataframe.empty:
            logger.error("Dataset is empty.")
            raise ValueError("Dataset is empty.")

        logger.info(
            "Dataset loaded successfully. Rows=%s Columns=%s",
            dataframe.shape[0],
            dataframe.shape[1],
        )

        return dataframe