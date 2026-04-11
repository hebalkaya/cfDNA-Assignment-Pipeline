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