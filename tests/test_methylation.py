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


def test_tumor_has_higher_hypermethylated_fraction():
    """Making sure tumor sample has higher rate of hypermethylation"""
    healthy = hypermethylated_fraction(HEALTHY_SAMPLE.methylation_values)
    tumor = hypermethylated_fraction(TUMOR_SAMPLE.methylation_values)
    assert tumor > healthy


def test_entropy_is_positive():
    """Making sure entropy nats is positive (> 0.0)"""
    entropy = methylation_entropy(HEALTHY_SAMPLE.methylation_values)
    assert entropy > 0.0


def test_variance_is_nonnegative():
    """Making sure variange is non negative( == 0 or > than 0)"""
    var = methylation_variance(HEALTHY_SAMPLE.methylation_values)
    assert var >= 0.0


def test_bimodality_score_tumor_greater():
    """Making sure tumor sample has higher bimodality score than healthy sample"""
    healthy = bimodality_score(HEALTHY_SAMPLE.methylation_values)
    tumor = bimodality_score(TUMOR_SAMPLE.methylation_values)
    assert tumor > healthy

