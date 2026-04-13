"""
Single entry point for the cfDNA multi-signal cancert detection pipeline.

Usage:
    python run_analysis.py
    docker compose run pipeline
"""


import os
import time
import pandas as pd 
from src.simulate import simulate_dataset
from src.fragmentomics import extract_fragmentomics_dataframe
from src.methylation import extract_methylation_dataframe
from src.classifier import *

TUMOR_FRACTIONS = [0.0, 0.001, 0.005, 0.01, 0.05, 0.10]
N_SAMPLES_PER_FRACTION = 150
RANDOM_SEED = 55
RESULTS_DIR = "results"