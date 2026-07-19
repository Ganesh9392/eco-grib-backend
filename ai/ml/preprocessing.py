"""
preprocessing.py

Responsible for preparing the dataset for machine learning.

Responsibilities
----------------
- Remove duplicates
- Handle missing values
- Encode categorical columns
- Split Features (X) and Target (y)
- Save encoder for future predictions

Author: Eco-Grid AI Module
"""

from __future__ import annotations

import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from pandas.api.types import (
    is_numeric_dtype,
    is_string_dtype,
)

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Handles preprocessing of the Eco-Grid dataset.
    """

    TARGET_COLUMN = "TargetBrightness"

    CATEGORICAL_COLUMNS = [
        "BuildingName",
        "RoomType",
        "FixtureType",
        "DayOfWeek",
        "Season",
        "Weather",
    ]

    DROP_COLUMNS = [
        "RoomID",
    ]

    def __init__(self, model_directory: str | Path):
        self.model_directory = Path(model_directory)
        self.model_directory.mkdir(parents=True, exist_ok=True)

    def process(
        self,
        dataframe: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.Series, ColumnTransformer]:
        """
        Prepare dataset for model training.

        Returns
        -------
        X
        y
        preprocessor
        """

        logger.info("Starting preprocessing...")

        dataframe = dataframe.copy()

        dataframe = self._remove_duplicates(dataframe)

        dataframe = self._handle_missing_values(dataframe)

        dataframe = dataframe.drop(
            columns=self.DROP_COLUMNS,
            errors="ignore",
        )

        X = dataframe.drop(columns=[self.TARGET_COLUMN])

        y = dataframe[self.TARGET_COLUMN]

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(
                        handle_unknown="ignore",
                    ),
                    self.CATEGORICAL_COLUMNS,
                ),
            ],
            remainder="passthrough",
        )

        logger.info("Fitting preprocessing pipeline...")

        preprocessor.fit(X)

        self._save_preprocessor(preprocessor)

        logger.info("Preprocessing completed successfully.")

        return X, y, preprocessor

    @staticmethod
    def _remove_duplicates(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        before = len(dataframe)

        dataframe = dataframe.drop_duplicates()

        removed = before - len(dataframe)

        logger.info("Removed %s duplicate rows.", removed)

        return dataframe

    @staticmethod
    def _handle_missing_values(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Handle missing values for both numeric and categorical columns.

        Numeric columns:
            Fill missing values with the median.

        Categorical/String columns:
            Fill missing values with the most frequent value (mode).
            If the column is completely empty, use "Unknown".
        """

        for column in dataframe.columns:

            # Numeric columns
            if is_numeric_dtype(dataframe[column]):

                median = dataframe[column].median()

                dataframe[column] = dataframe[column].fillna(median)

            # String / Categorical columns
            elif is_string_dtype(dataframe[column]):

                mode = dataframe[column].mode()

                if not mode.empty:

                    dataframe[column] = dataframe[column].fillna(mode.iloc[0])

                else:

                    dataframe[column] = dataframe[column].fillna("Unknown")

            # Fallback for any other dtype
            else:

                dataframe[column] = dataframe[column].fillna("Unknown")

        return dataframe

    def _save_preprocessor(
        self,
        preprocessor: ColumnTransformer,
    ) -> None:

        path = self.model_directory / "preprocessor.pkl"

        joblib.dump(preprocessor, path)

        logger.info(
            "Preprocessor saved at %s",
            path,
        )