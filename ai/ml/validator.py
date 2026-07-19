"""
validator.py

Responsible for validating the Eco-Grid AI training dataset.

Responsibilities
----------------
- Validate required columns
- Check for empty dataset
- Check duplicate rows
- Check missing values
- Validate numeric ranges
- Validate categorical values

Author: Eco-Grid AI Module
"""

from __future__ import annotations

import logging

import pandas as pd


logger = logging.getLogger(__name__)


class DatasetValidator:
    """
    Validates the training dataset before preprocessing and model training.
    """

    REQUIRED_COLUMNS = [
        "BuildingID",
        "BuildingName",
        "Floor",
        "RoomID",
        "RoomType",
        "FixtureType",
        "Occupancy",
        "OccupancyCount",
        "AmbientLux",
        "Hour",
        "DayOfWeek",
        "Month",
        "Season",
        "Weather",
        "CurrentBrightness",
        "PreviousBrightness",
        "Energy_kWh",
        "Voltage_V",
        "Current_A",
        "PowerFactor",
        "OperatingHours",
        "FixtureWattage",
        "UserOverrideCount",
        "TargetBrightness",
    ]

    VALID_ROOM_TYPES = {
        "Office",
        "Meeting Room",
        "Conference",
        "Cabin",
        "Reception",
        "Corridor",
        "Training Room",
    }

    VALID_FIXTURE_TYPES = {
        "LED Panel",
        "Downlight",
        "Tube Light",
        "Spot Light",
        "Emergency Light",
    }

    VALID_DAYS = {
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    }

    VALID_SEASONS = {
        "Summer",
        "Monsoon",
        "Winter",
    }

    VALID_WEATHER = {
        "Sunny",
        "Cloudy",
        "Rainy",
        "Clear",
    }

    @classmethod
    def validate(cls, dataframe: pd.DataFrame) -> None:
        """
        Runs all validations.

        Raises
        ------
        ValueError
            If any validation fails.
        """

        logger.info("Starting dataset validation...")

        cls._validate_empty(dataframe)
        cls._validate_columns(dataframe)
        cls._validate_duplicates(dataframe)
        cls._validate_missing_values(dataframe)
        cls._validate_ranges(dataframe)
        cls._validate_categories(dataframe)

        logger.info("Dataset validation completed successfully.")

    @staticmethod
    def _validate_empty(dataframe: pd.DataFrame) -> None:
        if dataframe.empty:
            raise ValueError("Dataset is empty.")

    @classmethod
    def _validate_columns(cls, dataframe: pd.DataFrame) -> None:
        missing = set(cls.REQUIRED_COLUMNS) - set(dataframe.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

    @staticmethod
    def _validate_duplicates(dataframe: pd.DataFrame) -> None:
        duplicates = dataframe.duplicated().sum()

        if duplicates:
            raise ValueError(
                f"Dataset contains {duplicates} duplicate rows."
            )

    @staticmethod
    def _validate_missing_values(dataframe: pd.DataFrame) -> None:
        missing = dataframe.isnull().sum()
        missing = missing[missing > 0]

        if not missing.empty:
            raise ValueError(
                f"Missing values detected:\n{missing.to_string()}"
            )

    @classmethod
    def _validate_categories(cls, dataframe: pd.DataFrame) -> None:

        cls._validate_column_values(
            dataframe,
            "RoomType",
            cls.VALID_ROOM_TYPES,
        )

        cls._validate_column_values(
            dataframe,
            "FixtureType",
            cls.VALID_FIXTURE_TYPES,
        )

        cls._validate_column_values(
            dataframe,
            "DayOfWeek",
            cls.VALID_DAYS,
        )

        cls._validate_column_values(
            dataframe,
            "Season",
            cls.VALID_SEASONS,
        )

        cls._validate_column_values(
            dataframe,
            "Weather",
            cls.VALID_WEATHER,
        )

    @staticmethod
    def _validate_column_values(
        dataframe: pd.DataFrame,
        column: str,
        valid_values: set,
    ) -> None:

        invalid = set(dataframe[column].unique()) - valid_values

        if invalid:
            raise ValueError(
                f"{column} contains invalid values: {sorted(invalid)}"
            )

    @staticmethod
    def _validate_ranges(dataframe: pd.DataFrame) -> None:

        DatasetValidator._check_range(
            dataframe,
            "Occupancy",
            0,
            1,
        )

        DatasetValidator._check_range(
            dataframe,
            "OccupancyCount",
            0,
            100,
        )

        DatasetValidator._check_range(
            dataframe,
            "AmbientLux",
            0,
            100000,
        )

        DatasetValidator._check_range(
            dataframe,
            "Hour",
            0,
            23,
        )

        DatasetValidator._check_range(
            dataframe,
            "Month",
            1,
            12,
        )

        DatasetValidator._check_range(
            dataframe,
            "CurrentBrightness",
            0,
            100,
        )

        DatasetValidator._check_range(
            dataframe,
            "PreviousBrightness",
            0,
            100,
        )

        DatasetValidator._check_range(
            dataframe,
            "TargetBrightness",
            0,
            100,
        )

        DatasetValidator._check_range(
            dataframe,
            "Energy_kWh",
            0,
            1000,
        )

        DatasetValidator._check_range(
            dataframe,
            "Voltage_V",
            150,
            260,
        )

        DatasetValidator._check_range(
            dataframe,
            "Current_A",
            0,
            100,
        )

        DatasetValidator._check_range(
            dataframe,
            "PowerFactor",
            0,
            1,
        )

        DatasetValidator._check_range(
            dataframe,
            "OperatingHours",
            0,
            100000,
        )

        DatasetValidator._check_range(
            dataframe,
            "FixtureWattage",
            1,
            1000,
        )

        DatasetValidator._check_range(
            dataframe,
            "UserOverrideCount",
            0,
            1000,
        )

    @staticmethod
    def _check_range(
        dataframe: pd.DataFrame,
        column: str,
        minimum: float,
        maximum: float,
    ) -> None:

        invalid = dataframe[
            (dataframe[column] < minimum)
            | (dataframe[column] > maximum)
        ]

        if not invalid.empty:
            raise ValueError(
                f"{column} contains values outside "
                f"the allowed range ({minimum}-{maximum})."
            )