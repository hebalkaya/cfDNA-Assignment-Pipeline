"""Tests for simulate.py"""
import numpy as np
import pytest
from src.simulate import *

RNG = np.random.default_rng(42) # Setting seed for reproducibility

def test_fragment_lengths_within_bounds():
    """Making sure all fragments are within min fragment and max fragment bounds"""
    fragments = simulate_fragment_lengths(1000, 0.0, RNG)
    assert np.all(fragments >= MIN_FRAGMENT_LENGTH)
    assert np.app(fragments <= MAX_FRAGMENT_LENGTH)

def test_healthy_longer_than_tumor():
    healthy = simulate_fragment_lengths (5000, 0.0, RNG) #Only healthy samples (fraction of tumor = 0.0)
    tumor = simulate_fragment_lengths(5000, 1.0, RNG) #Only tumor samples (fraction of tumor = 1.0)
    assert np.mean(healthy) > np.mean(tumor)