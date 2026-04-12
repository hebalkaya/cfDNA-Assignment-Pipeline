# Logbook
### Friday, April 10

#### Set up Google Cloud
- [X] Set up Google Cloud
- [X] Set up Google Cloud Project ```cfdna-pipeline``` (ID: cfdna-pipeline-492919)
- [X] Set up Google Cloud Data Bucket ```cfdna-results-he``` (Not publicly accessible)
- [X] Install gcloud CLI
> For various serverless products, the gcloud CLI is the primary interface by which you upload code to run and generally support your development workflow.
- [X] Authenticate gcloud CLI
```
You are now authenticated with the gcloud CLI!
```
#### Authenticate Git
- [X] Initiate Git
- [X] Clone Git repo

#### Build the complete structure
- [X] Build the skeleton

#### Begin coding
- [X] Initiated src/simulate.py
- [X] Initiated tests/test_simulate.py

#### Build Docker and run tests inside it
- [X] Build the Docker image
```
docker build -t cfdna-pipeline .
```
- [X] Run tests inside the container
```
docker compose run test
```
- [X] Complete src/simulate.py
- [X] Complete tests/test_simulate.py

### Saturday, April 11
- [X] Initiate src/fragmentomics.py
- [X] Initiate tests/test_fragmentomics.py
- [X] Complete src/fragmentomics.py
- [X] Complete tests/test_fragmentomics.py
- [X] Initiate src/classifier.py
- [X] Complete classifier model 1: Random Forest on Fragmentomics
- [X] Complete full docker composer build
- [X] Complete full docker composer run
```
docker compose build --no-cache
```
```
docker compose run --remove-orphans pipeline python src/classifier.py
``` 

#### Model 1 Results: Random Forest on Fragmentomics only 
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
### Sunday, April 12
- [X] Initiate src/methylation.py
- [X] Initiate tests/test_methylation.py
- [X] Complete src/methylation.py
- [X] Complete tests/test_methylation.py
- [X] Complete initial methylation run

#### Changin Methylation parameters in ```methylation.py```
**Initial results**
```
                mean_methylation  hypermethylated_fraction  methylation_variance  bimodality_score
tumor_fraction                                                                                    
0.000                     0.1500                       0.0                0.0025           -0.1498
0.001                     0.1500                       0.0                0.0025           -0.1497
0.005                     0.1531                       0.0                0.0025           -0.1528
0.010                     0.1559                       0.0                0.0025           -0.1556
0.050                     0.1784                       0.0                0.0023           -0.1776
0.100                     0.2067                       0.0                0.0022           -0.2043
```
- The methylation signal is too weak. At 10% tumour fraction, mean methylation **only moves from 0.15 to 0.21**. Hypermethylated fraction is 0.0 across the board, the signal is essentially invisible.
- The methylation mixing formula is correct but the parameters are too conservative.
- At 10% tumour fraction we are getting 90% healthy × 0.15 + 10% tumour × 0.72 = 0.207. Mathematically correct but biologically the tumour methylation signal needs to be stronger and more distinct to be useful as a classifier feature.
```
# Methylation parameters
N_CPG_SITES = 500
HEALTHY_METHYLATION_MEAN = 0.10   # was 0.15 — make healthy lower
HEALTHY_METHYLATION_STD = 0.03    # was 0.05 — tighter
TUMOUR_METHYLATION_MEAN = 0.85    # was 0.72 — make tumour higher
TUMOUR_METHYLATION_STD = 0.08     # was 0.12 — tighter
```
**Updated results**
```
ethylation features by tumor fraction:
                mean_methylation  hypermethylated_fraction  methylation_variance  bimodality_score
tumor_fraction                                                                                    
0.000                     0.0994                    0.0000                0.0009           -0.0994
0.001                     0.1007                    0.0014                0.0017            0.2937
0.005                     0.1042                    0.0056                0.0040            0.6403
0.010                     0.1075                    0.0102                0.0066            0.7522
0.050                     0.1389                    0.0525                0.0285            0.7423
0.100                     0.1751                    0.1010                0.0522            0.7484
```
