"""
predictor.py

Handles real-time AI predictions.

Author: Eco-Grid AI Module
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)


class BrightnessPredictor:
    """
    Predict brightness using the trained model.
    """

    def __init__(self, model, preprocessor):

        self.model = model
        self.preprocessor = preprocessor

    def predict(self, sensor_data: dict) -> dict:
        """
        Predict brightness.

        Parameters
        ----------
        sensor_data : dict

        Returns
        -------
        dict
        """

        dataframe = pd.DataFrame([sensor_data])

        transformed = self.preprocessor.transform(dataframe)

        prediction = self.model.predict(transformed)[0]

        prediction = max(0, min(100, round(float(prediction), 2)))

        return {
            "recommended_brightness": prediction
        }