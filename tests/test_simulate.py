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

