"""
Extracts DNA methylation from cfDNA samples.

Biological basis:
    Cancer cells exhibit widespread unusual DNA methylation, including
    hypermethylation of tumor supressor gene promoters and CpG islands.
    This methylation pattern is reflected in tumor-derived cfDNA and
    provides a cancer-specific signal detectable from sequenceing data.

    Source papers:
    * Hanahan & Weinberg, 2011, Cell (Hallmarks of Cancer: The Next Generation)
    * Moss et al., 2018, Nature Communications 2018 (Comprehensive human cell-type methylation atlas reveals origins of circulating cell-free DNA in health and disease)

    See the code for biologically methylation thresholds
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from src.simulate import SampleData

# Methylation thresholds
HYPERMETHYLATION_THRESHOLD = 0.5    # CpGs above this are "hypermethylated"
ENTROPY_BINS = 20                   # bins for entropy calculation

def mean_methylation(methylation_values: np.ndarray) -> float:
    """
    Mean methylation across all CpG sites.

    The simplest summary of metylation level.
    This level increases with tumor fraction.

    Args:
        methylation_values: array of methylation values (0.0 - 1.0)
    
    Returns:
        Mean metylation (0.0 - 1.0)
    """
    return float(np.mean(methylation_values))
