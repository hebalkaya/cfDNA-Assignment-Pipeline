"""
Trains and evaluates Random Forest Classifiers for cancer detection
from cfDNA features.

Supports three model configurations:
    * Model 1: Fragmentomics features only
    * Model 2: Methylation features only    (added later)
    * Model 3: Combined features            (added later)

Key evaluation metric: sensitivity at each tumor fraction threshold.
Overall accuracy is less meaningful. The clinically relevant question is:
Can we detect cancer when tumor fraction is 0.1?
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    roc_curve,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

# Feature column definitions
FRAGMENTOMICS_FEATURES = [
    'median_fragment_length',
    'short_fragment_ratio',
    'long_fragment_ratio',
    'fragment_length_entropy',
    'nucleosomal_peak_ratio',
    'short_to_long_ratio'
]

# Random Forest hyperparameters
RF_PARAMS = {
    'n_estimators': 200,
    'max_depth': 6,
    'min_samples_leaf': 3,
    'random_state': 42,
    'n_jobs': -1,
    'class_weight': 'balanced'
}

def prepare_features(
    df: pd.DataFrame,
    feature_columns: List[str]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract feature matrix and label vector from DataFrame.

    Args:
        df: DataFrame with feature columns and 'is_cancer' column
        feature_columns: list of column names to use as features
    
    Returns:
        X: feature matrix (n_samples, n_features)
        y: label vector (n_samples,) - 1 = cancer, 0 = healthy
    """
    X = df[feature_columns].values.astype(float)
    y = df['is_cancer'].astype(int).values
    return X, y

def compute_sensitivity_by_tumor_fraction(
    df: pd.DataFrame,
    y_prob: np.ndarray,
    threshold: float = 0.5
) -> Dict[float, float]:
    """
    Computes sensitivity (recall) separately at each tumor fraction.

    Key clinical metric. It tells us at what tumor fraction the model
    can reliably detect cancer.

    Args:
        df: DataFrame with 'tumor_fraction' and 'is_cancer' columns
        y_prob: predicted cancer probabilities from cross-validation
        threshold: classification threshold (default = 0.5)
    
    Returns:
        Dictionary of tumor_fraction -> sensitivity
    """
    df = df.copy()
    df['y_prob'] = y_prob
    df['y_pred'] = (y_prob >= threshold).astype(int)

    sensitivity_by_tf = {}

    # Only computing for cancer samples (tf > 0)
    cancer_df = df[df['is_cancer'] == True]

    for tf in sorted(cancer_df['tumor_fraction'].unique()):
        subset = cancer_df[cancer_df['tumor_fraction'] == tf]
        if len(subset) == 0:
            continue
        sensitivity = (subset['y_pred'] == 1).mean()
        sensitivity_by_tf[tf] = float(sensitivity)
    
    return sensitivity_by_tf


def train_and_evaluate(
    df: pd.DataFrame,
    feature_columns: List[str],
    model_name: str,
    cv_folds: int = 5
) -> Dict:
    """
    Trains a Random Forest Classifier and evaluates with cross-validation.

    Uses stratified k-fold cross-validation to ensure each fold contains
    samples from all tumor fraction groups.

    Args:
        df: DataFrame with features and metadata
        feature_columns: feature columns to use
        model_name: name for this model (used in output)
        cv_folds: number of cross-validation folds
    
    Returns:
        Dictionary containing:
            * model: trained RandomForestClassifier
            * y_true: true labels
            * y_prob: predicted probabilities (cancer class)
            * auc: ROC AUC score (Area under the curve)
            * fpr, tpr: ROC curve points (fpr: false positive rate, tpr: true positive rate)
            * sensitivity_by_tf: sensitivity at each tumor fraction
            * feature_importance: dict of feature name -> importance
    """
    X, y = prepare_features(df, feature_columns)

    # Scaling features to improve RF stability
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Cross-validation are obtained from out-of-fold predictions
    cv = StratifiedKFold(n_splits = cv_folds, shuffle = True, random_state = 42)
    model = RandomForestClassifier(**RF_PARAMS)

    # Getting predicted probabilities from cross-validation
    y_prob = cross_val_predict(
        model, X_scaled, y,
        cv = cv,
        method = 'predict_proba'
    )[:, 1] # Probability of cancer class

    # Computing ROC curve
    fpr, tpr, thresholds = roc_curve(y, y_prob)
    auc = roc_auc_score(y, y_prob)

    # Computing sensitivity at each tumor fraction
    sensitivity_by_tf = compute_sensitivity_by_tumor_fraction(
        df, y_prob, threshold = 0.5
    )

    # Training final model on all data for feature importance
    model.fit(X_scaled, y)
    feature_importance = dict(zip(feature_columns, model.feature_importances_))

    print(f"\n{'='*50}")
    print(f"Model: {model_name}")
    print(f"Features: {len(feature_columns)}")
    print(f"Samples: {len(y)} ({y.sum()} cancer, {(~y.astype(bool)).sum()} healthy)")
    print(f"ROC AUC: {auc:.4f}")
    print(f"\nSensitivity by tumor fraction:")
    for tf, sens in sensitivity_by_tf.items():
        print(f"  TF={tf}: {sens:.3f}")
    print(f"\nTop features by importance:")
    sorted_importance = sorted(
        feature_importance.items(),
        key = lambda x: x[1],
        reverse = True
    )
    for feat, imp in sorted_importance:
        print(f"  {feat}: {imp:.4f}")
    
    return {
        'model_name': model_name,
        'model': model,
        'scaler': scaler,
        'feature_columns': feature_columns,
        'y_true': y,
        'y_prob': y_prob,
        'auc': auc,
        'fpr': fpr,
        'tpr': tpr,
        'sensitivity_by_tf': sensitivity_by_tf,
        'feature_importance': feature_importance
    }

if __name__ == "__main__":
    from src.simulate import simulate_dataset
    from src.fragmentomics import extract_fragmentomics_dataframe

    print("Generating dataset ...")
    TUMOR_FRACTIONS = [0.0, 0.001, 0.005, 0.01, 0.05, 0.10]
    samples = simulate_dataset(
        TUMOR_FRACTIONS,
        n_samples_per_fraction = 300,
        seed = 42
    )

    print("Extracting fragmentomics features ...")
    frag_df = extract_fragmentomics_dataframe(samples)

    print("Training Model 1: Fragmentomics only ...")
    results = train_and_evaluate(
        frag_df,
        FRAGMENTOMICS_FEATURES,
        model_name = "Model 1 - Fragmentomics Only"
    )

    print(f"\nFinal AUC: {results['auc']:4f}")