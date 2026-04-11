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
