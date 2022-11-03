from pathlib import Path


def generate_reports_dir():
    Path("reports/extracted_features/lme/base").mkdir(parents=True, exist_ok=True)
    Path("reports/extracted_features/lme/fa").mkdir(parents=True, exist_ok=True)
    Path("reports/extracted_features/lme/rpsd").mkdir(parents=True, exist_ok=True)
    Path("reports/extracted_features/ml").mkdir(parents=True, exist_ok=True)
    Path("reports/feature_selection/lme/base").mkdir(parents=True, exist_ok=True)
    Path("reports/feature_selection/lme/fa").mkdir(parents=True, exist_ok=True)
    Path("reports/feature_selection/lme/rpsd").mkdir(parents=True, exist_ok=True)
    Path("reports/feature_selection/rfecv").mkdir(parents=True, exist_ok=True)
    Path("reports/feature_selection/figures").mkdir(parents=True, exist_ok=True)
    Path("reports/logs/base").mkdir(parents=True, exist_ok=True)
    Path("reports/logs/fa").mkdir(parents=True, exist_ok=True)
    Path("reports/logs/rpsd").mkdir(parents=True, exist_ok=True)
    Path("reports/metrics/lme").mkdir(parents=True, exist_ok=True)
    Path("reports/metrics/rfecv").mkdir(parents=True, exist_ok=True)
    Path("reports/random_indices").mkdir(parents=True, exist_ok=True)