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