"""
Generates synthetic cfDNA datasets with known tumor fractions.

Biological basis (from literature):
* Healthy cfDNA: fragment lengths ~167bp (nucleosomal peak, the length of DNA associated with a nucleosome plus linker)
* Tumor cfDNA: enriched ~143bp (sub-nucleosomal, altered chromatin)
* Cancer methylation: hypermetilation at tumor specific CpG islands

Parameters derived from / Source papers:
* Underhill et al. 2016, PLOS (mouse cfDNA & ctDNA fragment lengths) (Fragment Length of Circulating Tumor DNA)
* Snyder et al. 2016, Cell (cfDNA fragment lengths) (Cell-free DNA Comprises an In Vivo Nucleosome Footprint that Informs Its Tissues-Of-Origin)
* Hanahan & Weinberg 2011 (methylation as cancer hallmark)
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List


# Fragment length parameters (from published values)
HEALTHY_FRAGMENT_MEAN = 167
HEALTHY_FRAGMENT_STDEV = 20
TUMOR_FRAGMENT_MEAN = 143
TUMOR_FRAGMENT_STDEV = 30
MIN_FRAGMENT_LENGTH = 50
MAX_FRAGMENT_LENGTH = 400

# Methylation parameters
N_CPG_SITES = 500
HEALTHY_METHYLATION_MEAN = 0.15
HEALTHY_METHYLATION_STDEV = 0.05
TUMOR_METHYLATION_MEAN = 0.72
TUMOR_METHYLATION_STDEV = 0.12

@dataclass
class SampleData:
    """Container for one simulated cfDNA/ctDNA sample."""
    sample_id: str
    tumor_fraction: float
    fragment_lengths: np.ndarray
    methylation_values: np.ndarray
    is_cancer: bool

def simulate_fragment_lengths(
    n_fragments: int,
    tumor_fraction: float,
    rng: np.random.Generator
) -> np.ndarray:
    """
    Simulates cfDNA/ctDNA fragment length distribution.

    Mixes healthy and tumor-derived fragments at the given tumor fraction.

    Args:
        n_fragments: number of fragments to simulate
        tumor_fraction: proportion of tumor-derived fragments (0.0-1.0)
        rng: numpy random generator

    Returns:
        Array of fragment lengths in base pair (bp)
    """