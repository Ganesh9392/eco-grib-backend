"""
trainer.py

Responsible for training the Eco-Grid AI model.

Responsibilities
----------------
- Split dataset
- Apply preprocessing
- Train Random Forest
- Evaluate performance
- Save trained model
- Save training metadata

Author: Eco-Grid AI Module
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split


logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Trains the Eco-Grid Random Forest model.
    """

    MODEL_NAME = "brightness_model.pkl"
    METADATA_NAME = "model_metadata.json"

    def __init__(self, model_directory: str | Path):

        self.model_directory = Path(model_directory)
        self.model_directory.mkdir(parents=True, exist_ok=True)

    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        preprocessor: ColumnTransformer,
    ) -> dict:
        """
        Train Random Forest model.

        Returns
        -------
        dict
            Training metrics
        """

        logger.info("Splitting dataset...")

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            shuffle=True,
        )

        logger.info("Applying preprocessing...")

        X_train_processed = preprocessor.transform(X_train)
        X_test_processed = preprocessor.transform(X_test)

        logger.info("Training Random Forest...")

        model = RandomForestRegressor(
            n_estimators=300,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        )

        model.fit(
            X_train_processed,
            y_train,
        )

        logger.info("Evaluating model...")

        predictions = model.predict(X_test_processed)

        mae = mean_absolute_error(
            y_test,
            predictions,
        )

        mse = mean_squared_error(
            y_test,
            predictions,
        )

        rmse = mse ** 0.5

        r2 = r2_score(
            y_test,
            predictions,
        )

        metrics = {
            "model": "RandomForestRegressor",
            "trained_at": datetime.utcnow().isoformat(),
            "training_rows": len(X_train),
            "testing_rows": len(X_test),
            "mae": round(mae, 3),
            "mse": round(mse, 3),
            "rmse": round(rmse, 3),
            "r2_score": round(r2, 3),
        }

        logger.info("Saving model...")

        self._save_model(model)

        self._save_metadata(metrics)

        logger.info("Training completed successfully.")

        return metrics

    def _save_model(
        self,
        model: RandomForestRegressor,
    ) -> None:

        model_path = self.model_directory / self.MODEL_NAME

        joblib.dump(
            model,
            model_path,
        )

        logger.info(
            "Model saved at %s",
            model_path,
        )

    def _save_metadata(
        self,
        metrics: dict,
    ) -> None:

        metadata_path = (
            self.model_directory / self.METADATA_NAME
        )

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metrics,
                file,
                indent=4,
            )

        logger.info(
            "Metadata saved at %s",
            metadata_path,
        )