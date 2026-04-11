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