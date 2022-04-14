from src.extract_features import extract_features
from src.participants_age import participants_age
from src.lme import lme
from src.build_classification_models import build_classification_models


if __name__ == "__main__":
    participants_age()
    extract_features()
    lme()
    build_classification_models()