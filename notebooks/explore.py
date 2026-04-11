"""
Quick visual check that features separate cancer from healthy.

Running this locally to see the plots
mkdir -p results
pip install -r requirements.txt  # if not already installed locally
python notebooks/explore.py

"""
import matplotlib.pyplot as plt
import numpy as np
from src.simulate import simulate_dataset
from src.fragmentomics import extract_fragmentomics_dataframe
from src.methylation import extract_methylation_dataframe
import pandas as pd

# Generate dataset
TUMOUR_FRACTIONS = [0.0, 0.001, 0.005, 0.01, 0.05, 0.10]
samples = simulate_dataset(TUMOUR_FRACTIONS, n_samples_per_fraction=50)

frag_df = extract_fragmentomics_dataframe(samples)
meth_df = extract_methylation_dataframe(samples)
df = frag_df.merge(meth_df.drop(columns=['sample_id', 'tumour_fraction', 'is_cancer']),
                   left_index=True, right_index=True)

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle('Feature Distributions by Tumour Fraction', fontsize=14, fontweight='bold')

features = [
    ('short_fragment_ratio', 'Short Fragment Ratio'),
    ('median_fragment_length', 'Median Fragment Length (bp)'),
    ('nucleosomal_peak_ratio', 'Nucleosomal Peak Ratio'),
    ('mean_methylation', 'Mean Methylation'),
    ('hypermethylated_fraction', 'Hypermethylated Fraction'),
    ('bimodality_score', 'Bimodality Score'),
]

colors = plt.cm.viridis(np.linspace(0, 1, len(TUMOUR_FRACTIONS)))

for ax, (feature, title) in zip(axes.flat, features):
    for tf, color in zip(TUMOUR_FRACTIONS, colors):
        subset = df[df['tumour_fraction'] == tf][feature]
        ax.hist(subset, bins=20, alpha=0.6, label=f'TF={tf:.3f}', color=color)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(title)
    ax.set_ylabel('Count')
    if feature == features[0][0]:
        ax.legend(fontsize=7)

plt.tight_layout()
plt.savefig('results/feature_distributions.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved to results/feature_distributions.png")