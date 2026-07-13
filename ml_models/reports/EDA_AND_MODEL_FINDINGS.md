# EDA and Model Findings

Run `python ml_models/scripts/train_models.py` to generate the latest charts and metrics.

Expected outputs:

- `class_distribution.png`: Shows benign and malignant class balance.
- `correlation_heatmap.png`: Shows relationships between all medical attributes and diagnosis.
- `outlier_boxplots.png`: Highlights large-value spread in radius, perimeter, and area features.
- `feature_importance.png`: Shows the strongest predictors for the selected model.
- `model_comparison.csv`: Accuracy, precision, recall, F1, ROC-AUC, cross-validation ROC-AUC, and best parameters for Logistic Regression, SVM, and Random Forest.

Typical findings for the Wisconsin Breast Cancer dataset:

- The dataset has no missing values.
- Benign cases are more frequent than malignant cases, so stratified splitting is used.
- Radius, perimeter, area, concavity, concave points, and worst-case measurements are strongly associated with diagnosis.
- Several size-related features are highly correlated, which is why scaled linear/SVM pipelines and tree-based models are compared.
- Outliers appear in area and perimeter measurements; models are trained using robust validation rather than deleting clinically meaningful extremes.

