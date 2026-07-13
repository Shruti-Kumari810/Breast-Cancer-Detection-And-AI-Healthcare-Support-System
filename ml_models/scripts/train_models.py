from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
REPORTS = ROOT / "reports"
DATA = ROOT / "data"
for directory in (ARTIFACTS, REPORTS, DATA):
    directory.mkdir(parents=True, exist_ok=True)


def load_dataset() -> tuple[pd.DataFrame, pd.Series]:
    dataset = load_breast_cancer()
    features = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    target = pd.Series(dataset.target, name="target")
    full = features.copy()
    full["target"] = target
    full["diagnosis"] = target.map({0: "Malignant", 1: "Benign"})
    full.to_csv(DATA / "wisconsin_breast_cancer.csv", index=False)
    return features, target


def generate_eda(features: pd.DataFrame, target: pd.Series) -> dict:
    full = features.copy()
    full["target"] = target
    findings = {
        "rows": int(full.shape[0]),
        "columns": int(features.shape[1]),
        "missing_values": full.isna().sum().to_dict(),
        "class_distribution": target.map({0: "Malignant", 1: "Benign"}).value_counts().to_dict(),
        "top_correlations_with_target": full.corr(numeric_only=True)["target"].abs().sort_values(ascending=False).head(8).to_dict(),
    }

    plt.figure(figsize=(7, 4))
    sns.countplot(x=target.map({0: "Malignant", 1: "Benign"}))
    plt.title("Class Distribution")
    plt.tight_layout()
    plt.savefig(REPORTS / "class_distribution.png", dpi=160)
    plt.close()

    plt.figure(figsize=(14, 10))
    sns.heatmap(full.corr(numeric_only=True), cmap="viridis", linewidths=0.1)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(REPORTS / "correlation_heatmap.png", dpi=160)
    plt.close()

    outlier_counts = {}
    for column in features.columns:
        q1 = features[column].quantile(0.25)
        q3 = features[column].quantile(0.75)
        iqr = q3 - q1
        outlier_counts[column] = int(((features[column] < q1 - 1.5 * iqr) | (features[column] > q3 + 1.5 * iqr)).sum())
    findings["outlier_counts"] = outlier_counts

    selected = ["mean radius", "mean texture", "mean perimeter", "mean area", "worst radius", "worst area"]
    plt.figure(figsize=(12, 7))
    sns.boxplot(data=features[selected], orient="h")
    plt.title("Outlier Detection for Key Features")
    plt.tight_layout()
    plt.savefig(REPORTS / "outlier_boxplots.png", dpi=160)
    plt.close()

    (REPORTS / "eda_findings.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")
    return findings


def train() -> dict:
    x, y = load_dataset()
    generate_eda(x, y)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    grids = {
        "logistic_regression": (
            Pipeline([("scaler", StandardScaler()), ("classifier", LogisticRegression(max_iter=5000))]),
            {"classifier__C": [0.1, 1, 10], "classifier__solver": ["lbfgs"]},
        ),
        "svm": (
            Pipeline([("scaler", StandardScaler()), ("classifier", SVC(probability=True))]),
            {"classifier__C": [0.5, 1, 5], "classifier__kernel": ["rbf", "linear"]},
        ),
        "random_forest": (
            Pipeline([("classifier", RandomForestClassifier(random_state=42))]),
            {"classifier__n_estimators": [100, 200], "classifier__max_depth": [None, 6, 10]},
        ),
    }

    models = {}
    rows = []
    for name, (pipeline, params) in grids.items():
        search = GridSearchCV(pipeline, params, cv=cv, scoring="roc_auc", n_jobs=-1)
        search.fit(x_train, y_train)
        model = search.best_estimator_
        y_pred = model.predict(x_test)
        y_proba = model.predict_proba(x_test)[:, 1]
        models[name] = model
        rows.append(
            {
                "model": name,
                "best_params": search.best_params_,
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred),
                "recall": recall_score(y_test, y_pred),
                "f1": f1_score(y_test, y_pred),
                "roc_auc": roc_auc_score(y_test, y_proba),
                "cv_roc_auc_mean": cross_val_score(model, x, y, cv=cv, scoring="roc_auc").mean(),
            }
        )

    comparison = pd.DataFrame(rows).sort_values("roc_auc", ascending=False)
    best_model = comparison.iloc[0]["model"]
    comparison.to_csv(REPORTS / "model_comparison.csv", index=False)
    (REPORTS / "model_comparison.json").write_text(
        comparison.to_json(orient="records", indent=2), encoding="utf-8"
    )

    best = models[best_model]
    importance = permutation_importance(best, x_test, y_test, n_repeats=10, random_state=42)
    importance_frame = pd.DataFrame(
        {"feature": x.columns, "importance": importance.importances_mean}
    ).sort_values("importance", ascending=False)
    importance_frame.to_csv(REPORTS / "feature_importance.csv", index=False)
    plt.figure(figsize=(9, 6))
    sns.barplot(data=importance_frame.head(12), x="importance", y="feature")
    plt.title("Top Feature Importance")
    plt.tight_layout()
    plt.savefig(REPORTS / "feature_importance.png", dpi=160)
    plt.close()

    bundle = {
        "models": models,
        "best_model": best_model,
        "feature_names": list(x.columns),
        "metrics": comparison.to_dict(orient="records"),
    }
    joblib.dump(bundle, ARTIFACTS / "model_bundle.joblib")
    joblib.dump(best, ARTIFACTS / "best_model.joblib")
    return bundle


if __name__ == "__main__":
    result = train()
    print(f"Saved models. Best model: {result['best_model']}")

