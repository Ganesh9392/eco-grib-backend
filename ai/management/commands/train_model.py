from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from ai.ml.dataset_loader import DatasetLoader
from ai.ml.validator import DatasetValidator
from ai.ml.preprocessing import DataPreprocessor
from ai.ml.trainer import ModelTrainer


class Command(BaseCommand):
    help = "Train Eco-Grid AI Brightness Prediction Model"

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS("Starting AI Training..."))

        dataset_path = (
            Path(settings.BASE_DIR)
            / "ai"
            / "datasets"
            / "EcoGrid_Enterprise_AI_Dataset_3000 (1).xlsx"
        )

        model_directory = (
            Path(settings.BASE_DIR)
            / "ai"
            / "saved_models"
        )

        # Load Dataset
        loader = DatasetLoader(dataset_path)
        dataframe = loader.load()

        self.stdout.write(
            self.style.SUCCESS(
                f"Dataset Loaded : {len(dataframe)} rows"
            )
        )

        # Validate Dataset
        DatasetValidator.validate(dataframe)

        self.stdout.write(
            self.style.SUCCESS("Dataset Validation Successful")
        )

        # Preprocess
        preprocessor = DataPreprocessor(model_directory)

        X, y, transformer = preprocessor.process(dataframe)

        self.stdout.write(
            self.style.SUCCESS("Preprocessing Completed")
        )

        # Train
        trainer = ModelTrainer(model_directory)

        metrics = trainer.train(
            X=X,
            y=y,
            preprocessor=transformer,
        )

        self.stdout.write(
            self.style.SUCCESS("Training Completed")
        )

        self.stdout.write(str(metrics))