"""Test modules for fragmentomics.py"""
import numpy as np
import pytest
from src.simulate import simulate_dataset, SampleData
from src.fragmentomics import *

# Fixed test samples to be used in every test
HEALTHY_SAMPLE = simulate_dataset([0.0], n_samples_per_fraction = 1, seed = 42)[0]
TUMOR_SAMPLE = simulate_dataset([1.0], n_samples_per_fraction = 1, seed = 42)[0]

def test_short_fragment_ratio_range():
    """Making sure that short fragment length ratio falls within range 0.0 - 1.0"""
    ratio = short_fragment_ratio(HEALTHY_SAMPLE.fragment_lengths)
    assert 0.0 <= ratio <= 1.0

def test_tumor_has_higher_short_fragment_ratio():
    """Making sure tumor sample has higher short fragment ratio compared to a healthy sample"""
    healthy_ratio = short_fragment_ratio(HEALTHY_SAMPLE.fragment_lengths)
    tumor_ratio = short_fragment_ratio(TUMOR_SAMPLE.fragment_lengths)
    assert tumor_ratio > healthy_ratio

def test_healthy_has_higher_long_fragment_ratio():
    """Making sure healthy sample has higher long fragment ratio compared to a tumor sample"""
    healthy_ratio = long_fragment_ratio(HEALTHY_SAMPLE.fragment_lengths)
    tumor_ratio = long_fragment_ratio(TUMOR_SAMPLE.fragment_lengths)
    assert healthy_ratio > tumor_ratio

def test_entropy_is_positive():
    """Making sure shannon entropy for fragment lengths are positive"""
    entropy = fragment_length_entropy(HEALTHY_SAMPLE.fragment_lengths)
    assert entropy > 0.0

def test_nucleosomal_peak_ratio_healthy_greater():
    """Making sure the healthy (nucleosomal) peaks are greater in healthy sample"""
    healthy_ratio = nucleosomal_peak_ratio(HEALTHY_SAMPLE.fragment_lengths)
    tumor_ratio = nucleosomal_peak_ratio(TUMOR_SAMPLE.fragment_lengths)
    assert healthy_ratio > tumor_ratio

def test_short_to_long_ratio_tumor_greater():
    """Making sure the tumor short to long ratio is greater than short to long ratio in healthy sample"""
    healthy_ratio = short_to_long_ratio(HEALTHY_SAMPLE.fragment_lengths)
    tumor_ratio = short_to_long_ratio(TUMOR_SAMPLE.fragment_lengths)
    assert tumor_ratio > healthy_ratio

def test_extract_fragmentomics_features_returns_correct_keys():
    """Making sure extract_fragmentomics_features compiles and returns correct keys"""
    features = extract_fragmentomics_features(HEALTHY_SAMPLE)
    expected_keys = {
        'median_fragment_length', 'short_fragment_ratio',
        'long_fragment_ratio', 'fragment_length_entropy',
        'nucleosomal_peak_ratio', 'short_to_long_ratio',
        'sample_id', 'tumor_fraction', 'is_cancer'
    }
    assert set(features.keys()) == expected_keys

def test_extract_dataframe_shape ():
    """Making sure extract_fragmentomics_dataframe returns the correct shape.
    The n(rows) of df should match total sample size
    short_fragment_ratio, an example feature, should be one of the column names.
    """
    samples = simulate_dataset([0.0, 0.05], n_samples_per_fraction = 10)
    df = extract_fragmentomics_dataframe(samples)
    assert len(df) == 20
    assert 'short_fragment_ratio' in df.columns

# Edge case testing
def test_no_division_by_zero_all_short():
    """Edge case: all fragments are short."""
    fragments = np.full(100, 100) # all set as 100bp
    ratio = short_to_long_ratio(fragments)
    assert ratio >= 0.0

def test_nucleosomal_ratio_no_division_by_zero():
    """Edge case: no sub-nucleosomal fragments present."""
    fragments = np.full(100, 170) # all set as 170bp
    ratio = nucleosomal_peak_ratio(fragments)
    assert ratio >= 0.0