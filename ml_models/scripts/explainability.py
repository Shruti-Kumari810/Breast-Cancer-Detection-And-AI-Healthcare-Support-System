from pathlib import Path

import joblib
import pandas as pd
import shap


def generate_shap_summary(sample_csv: str | None = None) -> str:
    root = Path(__file__).resolve().parents[1]
    bundle = joblib.load(root / "artifacts" / "model_bundle.joblib")
    data_path = Path(sample_csv) if sample_csv else root / "data" / "wisconsin_breast_cancer.csv"
    data = pd.read_csv(data_path)
    x = data[bundle["feature_names"]].head(100)
    model = bundle["models"][bundle["best_model"]]
    classifier = model.named_steps.get("classifier", model)
    transformed = model[:-1].transform(x) if hasattr(model, "__getitem__") and len(model.steps) > 1 else x
    explainer = shap.Explainer(classifier, transformed)
    shap_values = explainer(transformed)
    output = root / "reports" / "shap_values.pkl"
    joblib.dump(shap_values, output)
    return str(output)


if __name__ == "__main__":
    print(generate_shap_summary())

