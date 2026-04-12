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
N_CPG_SITES = 1000
HEALTHY_METHYLATION_MEAN = 0.10     # was 0.15 — make healthy lower
HEALTHY_METHYLATION_STDEV = 0.03      # was 0.05 — tighter
TUMOR_METHYLATION_MEAN = 0.85       # was 0.72 — make tumor higher
TUMOR_METHYLATION_STDEV = 0.08        # was 0.12 — tighter


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
        tumor_fraction: proportion of tumor-derived fragments (0.0 - 1.0)
        rng: numpy random generator

    Returns:
        Array of fragment lengths in base pair (bp)
    """

    n_tumor = int(n_fragments * tumor_fraction)
    n_healthy = n_fragments - n_tumor

    healthy_fragments = rng.normal(HEALTHY_FRAGMENT_MEAN, HEALTHY_FRAGMENT_STDEV, n_healthy) # Random from normal distribution
    tumor_fragments = rng.normal(TUMOR_FRAGMENT_MEAN, TUMOR_FRAGMENT_STDEV, n_tumor)

    all_fragments = np.concatenate([healthy_fragments, tumor_fragments])
    return np.clip(all_fragments, MIN_FRAGMENT_LENGTH, MAX_FRAGMENT_LENGTH).astype(int) # Making sure to keep the fragments that are within the proper range 


def simulate_methylation(
    tumor_fraction: float,
    rng: np.random.Generator
) -> np.ndarray:
    """
    Simulates CpG methylation values for a cfDNA/ctDNA sample.

    Models cfDNA methylation as a mixture of healthy and tumor molecules.
    Each CpG site is drawn from either the healthy or tumor distribution
    independently, according to the tumor fraction.

    This binary sampling model is more realistic than previous linear mixing.
    Each cfDNA molecule is either from a tumor cell or a healthy cell.

    Args:
        tumor_fraction: proportion of tumor-derived cfDNA (0.0 - 1.0)
        rng: numpy random generator

    Returns:
        Array of methylation values (0.0 to 1.0)
    """
    # For each CpG site, decide if it came from tumor or healthy cell
    is_tumor_molecule = rng.random(N_CPG_SITES) < tumor_fraction

    healthy_methylation = rng.normal(HEALTHY_METHYLATION_MEAN, HEALTHY_METHYLATION_STDEV, N_CPG_SITES)
    tumor_methylation = rng.normal(TUMOR_METHYLATION_MEAN, TUMOR_METHYLATION_STDEV, N_CPG_SITES)

    mixed = np.where(is_tumor_molecule, tumor_methylation, healthy_methylation)
    return np.clip(mixed, 0.0, 1.0)


def simulate_dataset(
    tumor_fractions: List[float],
    n_samples_per_fraction: int = 50,
    n_fragments_per_sample: int = 1000,
    seed: int = 42
) -> List[SampleData]:

    """
    Simulates a full dataset accross multiple tumor fractions

    Args:
        tumor_fractions: list of tumor fractions (e.g. [0.0, 0.001, 0.01, 0.05])
        n_samples_per_fraction: samples per tumor fraction
        n_fragments_per_sample: cfDNA fragments per sample
        seed: random seed for reproducibility

    Returns:
        List of SampleData objects 
    """
    rng = np.random.default_rng(seed)
    samples = []

    for tf in tumor_fractions:
        for i in range(n_samples_per_fraction):
            samples.append(SampleData(
                sample_id = f"TF{tf:.4f}_S{i:03d}",
                tumor_fraction = tf,
                fragment_lengths = simulate_fragment_lengths(n_fragments_per_sample, tf, rng),
                methylation_values = simulate_methylation(tf, rng),
                is_cancer = (tf> 0.0)
            ))
    return samples


def samples_to_dataframe(samples: List[SampleData]
) -> pd.DataFrame:
    """
    Convert list of SampleData to summary Dataframe
    """
    return pd.DataFrame([{
        'sample_id': sample.sample_id,
        'tumor_fraction': sample.tumor_fraction,
        'is_cancer': sample.is_cancer,
        'n_fragments': len(sample.fragment_lengths),
        'mean_fragment_length': round(np.mean(sample.mean_fragment_length), 2),
        'median_fragment_length': float(np.median(sample.fragment_lengths)),
        'mean_methylation': round(float(np.mean(sample.methylation_values)), 4)
    } for sample in samples])


if __name__ == "__main__":
    TUMOR_FRACTIONS = [0.0, 0.001, 0.005, 0.01, 0.05, 0.10]
    samples = simulate_dataset(TUMOR_FRACTIONS, n_samples_per_fraction = 20)
    df = sample_to_dataframe(samples)
    print(df.groupby('tumor_fraction').agg({
        'mean_fragment_length': 'mean',
        'mean_methylation': 'mean'
        }).round(4))
    print(f"\nTotal samples: {len(samples)}")