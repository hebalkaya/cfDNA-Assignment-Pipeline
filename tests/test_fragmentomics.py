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