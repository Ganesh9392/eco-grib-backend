"""
model_loader.py

Loads the trained AI model and preprocessing pipeline into memory.

Author: Eco-Grid AI Module
"""

from __future__ import annotations

import logging
from pathlib import Path

import joblib


logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Loads the trained model and preprocessor.
    """

    MODEL_FILE = "brightness_model.pkl"
    PREPROCESSOR_FILE = "preprocessor.pkl"

    def __init__(self, model_directory: str | Path):

        self.model_directory = Path(model_directory)

        self.model = None
        self.preprocessor = None

    def load(self) -> tuple:
        """
        Load model and preprocessor.
        """

        model_path = self.model_directory / self.MODEL_FILE
        preprocessor_path = (
            self.model_directory / self.PREPROCESSOR_FILE
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        if not preprocessor_path.exists():
            raise FileNotFoundError(
                f"Preprocessor not found: {preprocessor_path}"
            )

        logger.info("Loading trained model...")

        self.model = joblib.load(model_path)

        logger.info("Loading preprocessing pipeline...")

        self.preprocessor = joblib.load(preprocessor_path)

        logger.info("AI Model loaded successfully.")

        return self.model, self.preprocessor