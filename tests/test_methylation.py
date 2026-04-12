"""Tests for methylation.py"""
import numpy as np
import pytest
from src.simulate import simulate_dataset
from src.methylation import *

HEALTHY_SAMPLE = simulate_dataset([0.0], n_samples_per_fraction = 1, seed = 42)[0]
TUMOR_SAMPLE = simulate_dataset([1,0], n_samples_per_fraction = 1, seed = 42)[0]

