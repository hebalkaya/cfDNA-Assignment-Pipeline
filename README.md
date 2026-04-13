# cfDNA Multi-Signal Cancer Detection Pipeline
Initiated on April 10, 2026 to showcase a bioinformatician's relevant abilities in an interview.

This is a bioinformatics pipeline for ultra-sensitive cancer detection from 
cell-free DNA (cfDNA) using fragmentomics and DNA methylation signals.

## Over the Idea
Tumour-derived cfDNA differs from healthy cfDNA in two independent ways: how it's fragmented and how it's methylated. By building a pipeline that extracts and combines both signals, we can detect cancer at lower tumour fractions than either signal alone.

1. **Fragment length:** Tumor cfDNA is shorter (~143bp) than healthy 
   cfDNA (~167bp) due to altered chromatin structure in cancer cells.
2. **DNA methylation:** Tumour cfDNA is hypermethylated at 
   cancer-specific CpG islands, a hallmark of cancer.

This pipeline extracts both signals, trains Random Forest classifiers 
on each independently and in combination, and benchmarks sensitivity 
at relevant tumour fractions (0.1%, 0.5%, 1%, 5%, 10%).

## Key results

| Model | AUC | Sensitivity at 0.1% TF | Sensitivity at 0.5% TF |
|---|---|---|---|
| Fragmentomics only | 0.726 | 35.7% | 40.3% |
| Methylation only | 0.964 | 68.0% | 99.0% |
| Combined | 0.964 | 67.3% | 99.0% |

**Finding 1:** Fragmentomics alone fails below 1% tumour fraction. 
Sensitivity is near random at clinically relevant concentrations.

**Finding 2:** Methylation is the dominant signal. AUC jumps from 
0.726 to 0.964, and sensitivity at 0.5% TF goes from 40% to 99%.

**Finding 3:** Combining both signals adds marginal improvement, 
confirming the signals are correlated rather than independent.

## Quick Start

### Requirements
- Docker Desktop
- Python 3.11+ (for local development only)

### Run the full pipeline

```bash
git clone https://github.com/hebalkaya/cfDNA-Assignment-Pipeline.git
cd cfDNA-Assignment-Pipeline
mkdir -p results
docker compose run pipeline
```

This runs the complete pipeline in ~60 seconds and writes results to 
`results/`:
- `summary.csv`

### Run tests

```bash
docker compose run test
```

All 30+ unit tests run inside the Docker container. CI also runs 
automatically on every push via GitHub Actions.

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
│
├── results/                    ← gitignored, created locally
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run_analysis.py             # Single entry point
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
- [X] Methylation features only → Random Forest
- [X] Combined features → Random Forest + Logistic Regression?
Comparing sensitivity and specificity at each tumour fraction threshold.

> Upcoming modules will be added once ready

### Module 5 — Nextflow pipeline
### Module 6 — Reporting

## References
- Snyder et al. (2016) Cell: Cell-free DNA Comprises an In Vivo Nucleosome Footprint that Informs Its Tissues-Of-Origin
- Mouliere et al. (2018) Science Translational Medicine: Enhanced detection of circulating tumor DNA by fragment size analysis
- Cristiano et al. (2019) Nature: Genome-wide cell-free DNA fragmentation in patients with cancer
- Chen et al. (2025) Genome Research: Nanopore-based consensus sequencing enables accurate multimodal tumor cell-free DNA profiling
- Hanahan & Weinberg (2011) Cell: Hallmarks of Cancer: The Next Generation
