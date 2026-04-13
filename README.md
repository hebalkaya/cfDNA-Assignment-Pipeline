# cfDNA Assignment Pipeline
Initiated on April 10, 2026 to showcase a bioinformatician's relevant abilities in an interview.

## Over the Idea
Tumour-derived cfDNA differs from healthy cfDNA in two independent ways: how it's fragmented and how it's methylated. By building a pipeline that extracts and combines both signals, we can detect cancer at lower tumour fractions than either signal alone.

## On the Data
### Option A: Simulate with real parameters
Rather than pure simulation, parameterising the simulation from published real data. The exact fragment length distributions, methylation values, and tumour fractions are taken from published papers and used as ground truth parameters.

### Option B: Use the Cyclomics public GitHub data
Obtaining example data from the [```Cyclomics GitHub repository```](https://github.com/cyclomics). Real nanopore cfDNA data. Could be used as validation set as well as option C.

## Over the Architecture

| System                   | Tool          |
|:-------------------------|:--------------|
|Cloud environment         |Google Cloud VM|
|Development environment   |Docker         |
|Version management        |GitHub         |
|Programming language      |Python         |
|Workflow manager          |Nextflow       |
|Classifier                |scikit-learn   |
|Unit tests                |pytest         |

## Over the Structure
```
cfDNA-Assignment-Pipeline/
├── .github/
│   └── workflows/
│       └── test.yml
├── src/
│   ├── __init__.py
│   ├── simulate.py
│   ├── fragmentomics.py
│   ├── methylation.py
│   ├── classifier.py
│   └── report.py
├── tests/
│   ├── __init__.py
│   ├── test_simulate.py
│   ├── test_fragmentomics.py
│   ├── test_methylation.py
│   └── test_classifier.py
|
├── results/                    ← gitignored, created locally
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run_analysis.py
├── setup.py
├── Logbook.md
├── Notes.md
└── README.md
```

### Module 1 — Data simulation (simulate.py)
Generating realistic cfDNA datasets with known tumour fractions (0%, 0.1%, 0.5%, 1%, 5%, 10%) by mixing:
* Healthy cfDNA fragments: Gaussian distribution centred at 167bp
* Tumour cfDNA fragments: shifted distribution with enrichment at 143bp and shorter fragments
* Methylation profiles: tumour samples have hypermethylation at cancer-specific CpG islands

### Module 2 — Fragmentomics feature extraction (fragmentomics.py)
Extracting the following features for each sample extract:
* Median fragment length
* Short/long fragment ratio (fragments <150bp vs >150bp)
* Nucleosomal periodicity score
* Fragment length entropy

### Module 3 — Methylation feature extraction (methylation.py) [Coming soon]
For each sample extract:

Mean methylation at cancer-specific CpG islands (using published cancer methylation signatures)
Methylation entropy
Hypermethylated CpG fraction

### Module 4 — Classifier (classifier.py)
Training three scikit-learn classifiers:
- [X] Fragmentomics features only → Random Forest
- [ ] Methylation features only → Random Forest
- [ ] Combined features → Random Forest + Logistic Regression?
Comparing sensitivity and specificity at each tumour fraction threshold.

> Upcoming modules will be added once ready

### Module 5 — Nextflow pipeline
### Module 6 — Reporting

### Model 1 Results: Random Forest on Fragmentomics only 
```
Generating dataset ...
Extracting fragmentomics features ...
Training Model 1: Fragmentomics only ...

=========================================
Model: Model 1 - Fragmentomics Only
Features: 6
Samples: 1800 (1500 cancer, 300 healthy)
ROC AUC: 0.7505

Sensitivity by tumor fraction:
  TF=0.001:     0.343
  TF=0.005:     0.473
  TF=0.01:      0.600
  TF=0.05:      0.940
  TF=0.1:       0.997

Top features by importance:
  fragment_length_entropy:      0.3325
  short_fragment_ratio:         0.2610
  short_to_long_ratio:          0.2065
  nucleosomal_peak_ratio:       0.0867
  long_fragment_ratio:          0.0705
  median_fragment_length:       0.0427

Final AUC: 0.750460
```
