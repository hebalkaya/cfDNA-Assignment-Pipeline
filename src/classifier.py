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