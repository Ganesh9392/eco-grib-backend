"""
ai_service.py

Service layer for the Eco-Grid AI module.

Responsibilities
----------------
- Load AI model
- Accept prediction requests
- Return AI predictions

Author: Eco-Grid AI Module
"""

from __future__ import annotations

import logging
from pathlib import Path

from ai.ml.model_loader import ModelLoader
from ai.ml.predictor import BrightnessPredictor

logger = logging.getLogger(__name__)


class AIService:
    """
    AI Service used throughout the application.
    """

    def __init__(self, model_directory: str | Path):

        loader = ModelLoader(model_directory)

        model, preprocessor = loader.load()

        self.predictor = BrightnessPredictor(
            model=model,
            preprocessor=preprocessor,
        )

        logger.info("AI Service initialized successfully.")

    def predict_brightness(self, sensor_data: dict) -> dict:
        """
        Predict recommended brightness.

        Parameters
        ----------
        sensor_data : dict

        Returns
        -------
        dict
        """

        return self.predictor.predict(sensor_data)