"""Tests for classifier.py"""
import numpy as np
import pandas as pd
import pytest
from src.simulate import simulate_dataset
from src.fragmentomics import extract_fragmentomics_dataframe
from src.classifier import *

# Shared fixture generated once for all tests
@pytest.fixture(scope = "module")
def frag_df():
    """
    Makes sure a simulated fragmentomics dataset is generated once per module to provide 
    consistent feature data across multiple test cases and minimizes redundant computation.
    
    Returns:
        pd.DataFrame: A dataframe containing fragmentomics features 
        for varying tumor fractions.
    """
    samples = simulate_dataset(
        [0.0, 0.01, 0.05, 0.10],
        n_samples_per_fraction = 30,
        seed = 42
    )
    return extract_fragmentomics_dataframe(samples)

@pytest.fixture(scope="module")
def model1_results(frag_df):
    """Training the first model"""
    return train_and_evaluate(
        frag_df,
        FRAGMENTOMICS_FEATURES,
        model_name="Test Model 1",
        cv_folds=3
    )

def test_prepare_features_shape(frag_df):
    """Making sure the feature shape conforms to expectation"""
    X, y = prepare_features(frag_df, FRAGMENTOMICS_FEATURES)
    assert X.shape[0] == len(frag_df)
    assert X.shape[1] == len(FRAGMENTOMICS_FEATURES)
    assert len(y) == len(frag_df)

def test_prepare_features_binary_labels(frag_df):
    """Making sure the binary information contains only 0 or 1 """
    _, y = prepare_features(frag_df, FRAGMENTOMICS_FEATURES)
    assert set(np.unique(y)).issubset({0, 1})

def test_results_has_required_keys(model1_results):
    """Making sure the test results have all of the expected keys"""
    required = {
        'model_name', 'model', 'scaler', 'feature_columns',
        'y_true', 'y_prob', 'auc', 'fpr', 'tpr',
        'sensitivity_by_tf', 'feature_importance'
    }
    assert required.issubset(set(model1_results.keys()))

def test_auc_is_reasonable(model1_results):
    """Making sure AUC is better than random (0.5) with clear signals."""
    assert model1_results['auc'] > 0.6

def test_auc_in_valid_range(model1_results):
    """Making sure auc is within valid range (0.0 - 1.0)"""
    assert np.all(model1_results['y_prob'] >= 0.0)
    assert np.all(model1_results['y_prob'] <= 1.0)

def test_y_prob_in_valid_range(model1_results):
    """Making sure y_prob is within valid range (0.0 - 1.0)"""
    assert np.all(model1_results['y_prob'] >= 0.0)
    assert np.all(model1_results['y_prob'] <= 1.0)

def test_sensitivity_by_tf_keys(model1_results):
    """Making sure sensitivity is computed for each cancer tumor fraction"""
    expected_tfs = {0.01, 0.05, 0.10}
    actual_tfs = set(model1_results['sensitivity_by_tf'].keys())
    assert expected_tfs.issubset(actual_tfs)

def test_sensitivity_in_valid_range(model1_results):
    """
    Making sure all sensitivity scores are within expected range (0.0 - 1.0).
    Printing sensitivities that are out of bounds.
    """
    for tf, sens in model1_results['sensitivity_by_tf'].items():
        assert 0.0 <= sens <= 1.0, f"Sensitivity our of range at TF={tf}"

def test_sensitivity_increases_with_tumor_fraction(model1_results):
    """Making sure that higher tumor fraction should generally yield higher sensitivity"""
    tfs = sorted(model1_results['sensitivity_by_tf'].keys())
    if len (tfs) >= 2:
        low_tf_sens = model1_results['sensitivity_by_tf'][tfs[0]]
        high_tf_sens = model1_results['sensitivity_by_tf'][tfs[-1]] #last from the list
        assert high_tf_sens >= low_tf_sens

def test_feature_importance_sums_to_one(model1_results):
    """Making sure the sum of feature importance is < 1e-6"""
    total = sum(model1_results['feature_importance'].values())
    assert abs(total - 1.0) < 1e-6 # Avoiding rounding up errors.
