"""
Trains and evaluates Random Forest Classifiers for cancer detection
from cfDNA features.

Supports three model configurations:
    * Model 1: Fragmentomics features only
    * Model 2: Methylation features only    (added later)
    * Model 3: Combined features            (added later)

Key evaluation metric: sensitivity at each tumor fraction threshold.
Overall accuracy is less meaningful. The clinically relevant question is:
Can we detect cancer when tumor fraction is 0.1?
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from sklearn.ensemble import RandomForestClassifier

# Feature column definitions
FRAGMENTOMICS_FEATURES = [
    'median_fragment_length',
    'short_fragment_ratio',
    'long_fragment_ratio',
    'fragment_length_entropy',
    'nucleosomal_peak_ratio',
    'short_to_long_ratio'
]

# Random Forest hyperparameters
RF_PARAMS = {
    'n_estimators': 200,
    'max_depth': 6,
    'min_samples_leaf': 3,
    'random_state': 42,
    'n_jobs': -1
}