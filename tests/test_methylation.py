"""Tests for methylation.py"""
import numpy as np
import pytest
from src.simulate import simulate_dataset
from src.methylation import *

HEALTHY_SAMPLE = simulate_dataset([0.0], n_samples_per_fraction = 1, seed = 42)[0]
TUMOR_SAMPLE = simulate_dataset([1,0], n_samples_per_fraction = 1, seed = 42)[0]

def test_mean_methylation_in_range():
    """Making sure methylation is within the expected range (0.0 - 1.0)"""
    val = mean_methylation(HEALTHY_SAMPLE.methylation_values)
    assert 0.0 <= val <= 1.0

def test_hypermethylated_fraction_in_range():
    """Making sure hypermethylation is within the expected range (0.0 - 1.0)"""
    val = hypermethylated_fraction(HEALTHY_SAMPLE.methylation_values)
    assert 0.0 <= val <= 1.0

