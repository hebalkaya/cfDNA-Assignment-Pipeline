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
RANDOM_SEED = 42
RESULTS_DIR = "results"


def run_pipeline():
    start = time.time()
    os.makedirs(RESULTS_DIR, exist_ok = True)

    print ("=" * 42)
    print("  cfDNA Multi-Signal Cancer Detection")
    print ("=" * 42)

    print("[1/4] Simulating cfDNA dataset ...")
    samples = simulate_dataset(
        TUMOR_FRACTIONS,
        n_samples_per_fraction = N_SAMPLES_PER_FRACTION,
        seed = RANDOM_SEED
    )

    print(f"* {len(samples)} samples | "
          f"* {len(TUMOR_FRACTIONS)} tumor fractions")
    
    print("[2/4] Extracting fragmentomics features ...")
    frag_df = extract_fragmentomics_dataframe(samples)
    meth_df = extract_methylation_dataframe(samples)
    combined_df = frag_df.merge(
        meth_df.drop(columns = ['sample_id', 'tumor_fraction', 'is_cancer']),
        left_index = True, right_index = True
    )

    print(f"{len(FRAGMENTOMICS_FEATURES)} fragmentomics + "
          f"{len(METHYLATION_FEATURES)} methylation features")
    
    print("[3/4] Training classifiers ...")
    r1 = train_and_evaluate(
        frag_df, FRAGMENTOMICS_FEATURES,
        "Model 1 - Fragmentomics only"
    )
    r2 = train_and_evaluate(
        meth_df, METHYLATION_FEATURES,
        "Model 2 - Methylation only"
    )
    r3 = train_and_evaluate(
        combined_df, COMBINED_FEATURES,
        "Model 3 - Combined"
    )

    print("\n[4/4] Saving results ...")
    summary = pd.DataFrame([{
        'model': r['model_name'],
        'auc': round(r['auc'], 4),
        **{f"sens_tf_{k:.3f}": round(v, 3)
            for k, v in r['sensitivity_by_tf'].items()}
    } for r in [r1, r2, r3]])

    path = os.path.join(RESULTS_DIR, 'summary.csv')
    summary.to_csv(path, index=False)
    print(f"*Summary saved to {path}")

    elapsed = time.time() - start
    print(f"\n{'='*42}")
    print(f"    Pipeline completed in {elapsed:.1f}s")
    print(f"    Results in {RESULTS_DIR}/")
    print(f"{'='*42}\n")

    return [r1, r2, r3]


if __name__ == "__main__":
    run_pipeline()