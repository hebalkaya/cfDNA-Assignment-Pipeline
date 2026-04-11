"""
Extracts fragment length features from cfDNA samples.

Biological basis:
    Healthy cfDNA is predominantyl nucleosomal (~167bp), reflecting
    orderly apoptotic cleavage between nucleosomes. Tumor-derived cfDNA (ctDNA)
    shows enrichment of shorter sub-nucleosomal fragments (~143bp) due to altered
    chromatin structure in cancer cells.

    These differences in fragment length distribution provide a tumor-fraction-dependent
    signal detectable from sequencing data.

Source papers:
    * Underhill et al. 2016, PLOS (Mouse cfDNA & ctDNA fragment lengths) (Fragment Length of Circulating Tumor DNA)
    * Snyder et al. 2016, Cell (cfDNA fragment lengths) (Cell-free DNA Comprises an In Vivo Nucleosome Footprint that Informs Its Tissues-Of-Origin)
    * Cristiano et al., Nature 2019 (Genome-wide cell-free DNA fragmentation in patients with cancer)

See the code for biologically defined windows
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from src.simulate import SampleData

# Biologically defined windows (bp)
SHORT_THRESHOLD = 150           # fragments below 150bp are "short"
LONG_THRESHOLD = 180            # fragments above 180bp are "long"
NUCLEOSOMAL_LOW = 160           # nucleosomal window lower boundary
NUCLEOSOMAL_HIGH = 180          # nucelosomal window upper boundary
SUB_NUCLEOSOMAL_LOW = 120       # sub-nucleosomal window lower boundary
SUB_NUCLEOSOMAL_HIGH = 150      # sub-nucleosomal window upper boundary
ENTROPY_BINS = 50               # bins for entropy calculation

def short_fragment_ratio(fragment_lengths: np.ndarray) -> float:
    """
    Fraction of fragments below SHORT_THRESHOLD (150bp).

    Tumor cfDNA(ctDNA) is enriched in short fragments due to altered
    chromatin structure. This ratio increases with tumor fraction.

    Args:
        fragment_lengths: array of fragment lengths in bp
    
    Returns:
        Proportion of fragments below threshold (0.0 - 1.0)
    """
    # In NumPy, True is 1 and False is 0. When you take the mean of a
    # list of ones and zeros, we get the proportion of True values.
    return float(np.mean(fragment_lengths < SHORT_THRESHOLD))

def long_fragment_ratio(fragment_lengths: np.ndarray) -> float:
    """
    Fraction of fragments above LONG_THRESHOLD (180bp).

    Healthy cfDNA has a higher proportion of long nucleosomal fragments.
    This ratio decreases with increasing tumor fraction.

    Args:
        fragment_lengths: array of fragment lengths in bp

    Returns:
        Proportion of fragments above threshold (0.0 - 1.0)
    
    Note: The short_fragment_ratio and the long_fragment_ratio functions
    could be merged into a fragment_length_ratio function to do both
    simultaneously. This approach was taken to maintain modularity.
    """
    return float(np.mean(fragment_lengths > LONG_THRESHOLD))

def fragment_length_entropy(fragment_lengths: np.ndarray) -> float:
    """
    Shannon entropy of the fragment length distribution.
    
    Captures distributional shape beyond central tendency.
    Tumor cfDNA (ctDNA) shows more variable fragmentation (higher entropy).
    
    S(X) = −∑ p(xi) log(p(xi))

    Args:
        fragment_lengths: array of fragment lengths in bp
    
    Returns:
        Shannon entropy (nats)
    """

    counts, _ = np.histogram(fragment_lengths, bins = ENTROPY_BINS)
    # Adding a small pseudocount to avoid log(0)
    probs = (counts + 1e-10) / (counts.sum() + ENTROPY_BINS * 1e-10)
    return float(-np.sum(probs * np.log(probs)))

def nucleosomal_peak_ratio(fragment_lengths: np.ndarray) -> float:
    """
    Ratio of nucleosomal to sub-nucleosomal fragments.

    In healthy samples: many nucleosomal (160 - 180bp) fragments.
    In tumor samples: enrichment of sub-nucleosomal (120 - 150bp) fragments.
    Ratio drops as tumor fraction increaases.

    Args:
        fragment_lengths: array of fragment lengths in bp
    
    Returns:
        Nucleosomal/sub-nucleosomal ratio (higher = healthier)
    """
    nucleosomal = np.sum(
        (fragment_lengths >= NUCLEOSOMAL_LOW) &
        (fragment_lengths <= NUCLEOSOMAL_HIGH)
    )

    sub_nucleosomal = np.sum(
        (fragment_lengths >= SUB_NUCLEOSOMAL_LOW) &
        (fragment_lengths <= NUCLEOSOMAL_HIGH)
    )
    # Avoiding division by zero
    if sub_nucleosomal == 0:
        return float(nucleosomal)
    return float(nucleosomal/sub_nucleosomal)

def short_to_long_ratio(fragment_lengths: np.ndarray) -> float:
    """
    Direct ratio of short (<150bp) to long (>180bp) fragments.

    Compact summary of the fragment length shift in tumor samples.
    Increases with tumor fraction (monotonous).

    Args:
        fragment_lengths: array of fragment lengths in bp
    
    Returns:
        Short/long ratio (higher = more tumor-like)
    """
    n_short = np.sum(fragment_lengths < SHORT_THRESHOLD)
    n_long = np.sum(fragment_lengths > LONG_THRESHOLD)
    # Avoiding division by zero
    if n_long == 0:
        return float(n_short)
    return float(n_short / n_long)
