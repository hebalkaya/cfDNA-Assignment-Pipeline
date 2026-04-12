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


def hypermethylated_fraction(methylation_values: np.ndarray) -> float:
    """
    Fraction of CpG sites with methylation above threshold (0.5).

    Direct measure of hypermethylation burden.
    Key feature: Healthy cfDNA has very few hypermethylated CpGs
    at cancer-specific loci. Tumor cfDNA/ctDNA has many.

    Args:
        methylation_values: array of methylation values (0.0 - 1.0)
    
    Returns:
        Proportion of hypermethylated CpGs (0.0 - 1.0)
    """
    return float(np.mean(methylation_values > HYPERMETHYLATION_THRESHOLD))


def methylation_entropy(methylation_values: np.ndarray) -> float:
    """
    Shannon entropy of the methylation value distribution.

    Healthy methylation: low and narrow (low entropy).
    Tumor methylation (hypermethylation): spread across higher values (higher entropy).

    S(X) = −∑ p(xi) log(p(xi))

    Args:
        methylation_values: array of methylation values (0.0 - 1.0)
    
    Returns:
        Shannon entropy (in natural algorithms/nats)
    """
    counts, _ = np.histogram(methylation_values, bins = ENTROPY_BINS, range = (0,1))
    probs = (counts + 1e-10) / (counts.sum() + ENTROPY_BINS * 1e-10)
    return float(-np.sum(probs * np.log(probs)))


def methylation_variance(methylation_values: np.ndarray) -> float:
    """
    Variance of methylation values across CpG sites.

    Tumor methylation is more heterogeneous (higher variance).
    Complements mean methylation as a distributional feature.

    Args:
        methylation_values: array of methylation values (0.0 - 1.0)
    
    Returns:
        Variance of methylation values
    """
    return float(np.var(methylation_values))

def bimodality_score(methylation_values: np.ndarray) -> float:
    """
    Score capturing bimodality of methylation distribution.

    Healthy samples: unimodal distribution around low methylation.
    Tumor samples: second peak appears at high methylation values,
    creating a bimodal distribution.

    Computed as: mean of high bin (>0.6) - mean of low bin (<0.3).
    Larger values indicate stronger bimodality / more tumor signal.

    Args:
        methylation_values: array of methylation values (0.0 - 1.0)

    Returns:
        Bimodality score (higher = more cancer-like)
    """
    high_peak = methylation_values[methylation_values > 0.6]
    low_peak = methylation_values[methylation_values < 0.3]

    mean_high = np.mean(high_peak) if len(high_peak) 0 else 0.0
    mean_low = np.mean(low_peak) if len(low_peak) > 0 else 0.0

    return float(mean_high - mean_low)
    