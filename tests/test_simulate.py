"""Tests for simulate.py"""
import numpy as np
import pytest
from src.simulate import *

RNG = np.random.default_rng(42) # Setting seed

def test_fragment_lengths_within_bounds():
    """Making sure all fragments are within min fragment and max fragment bounds"""
    fragments = simulate_fragment_lengths(1000, 0.0, RNG)
    assert np.all(fragments >= MIN_FRAGMENT_LENGTH)
    assert np.all(fragments <= MAX_FRAGMENT_LENGTH)

def test_healthy_longer_than_tumor():
    """Making sure the healthy fragments are always longer than the tumor fragments"""
    healthy = simulate_fragment_lengths (5000, 0.0, RNG) #Only healthy samples (fraction of tumor = 0.0)
    tumor = simulate_fragment_lengths(5000, 1.0, RNG) #Only tumor samples (fraction of tumor = 1.0)
    assert np.mean(healthy) > np.mean(tumor)

def test_methylation_increases_with_tumor_fraction():
    """Making sure the healthy fragments have lower methylation level"""
    low = np.mean(simulate_methylation(0.0, RNG)) #Only healthy samples
    high = np.mean(simulate_methylation(1.0, RNG)) #Only tumor samples
    assert high > low

def test_methylation_in_valid_range():
    """Making sure all methylations are within given bounds"""
    meth = simulate_methylation(0.5, RNG)
    assert np.all(meth >= 0.0)
    assert np.all(meth <= 1.0)

def test_dataset_correct_sample_count():
    """ Making sure we have correct sample counts when fractions and n per fraction is given"""
    samples = simulate_dataset([0.0, 0.01, 0.05], n_samples_per_fraction=10)
    assert len(samples) == 30