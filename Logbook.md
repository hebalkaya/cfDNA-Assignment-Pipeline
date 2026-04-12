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
**Updated results** (No linear mixing)
```
methylation features by tumor fraction:
                mean_methylation  hypermethylated_fraction  methylation_variance  bimodality_score
tumor_fraction                                                                                    
0.000                     0.0994                    0.0000                0.0009           -0.0994
0.001                     0.1007                    0.0014                0.0017            0.2937
0.005                     0.1042                    0.0056                0.0040            0.6403
0.010                     0.1075                    0.0102                0.0066            0.7522
0.050                     0.1389                    0.0525                0.0285            0.7423
0.100                     0.1751                    0.1010                0.0522            0.7484
```
- Much better. The signal is now visible and meaningful.
- Hypermethylated_fraction tracks tumour fraction almost perfectly. At TF = 0.1 exactly 10% of CpGs are hypermethylated.
- Bimodality_score jumps dramatically from -0.099 at TF = 0 to 0.29 at TF=0.001. **This is the most discriminative feature** at low tumour fractions. Even at 0.1% tumour fraction, the bimodality score is already 3x the healthy baseline.
- Mean_methylation moves but slowly (from 0.099 to 0.175 at 10%). Useful but not the strongest feature.
- **Consensus:** Methylation features are most powerful at detecting the presence of any tumour signal (bimodality_score is very sensitive at low TF), while fragmentomics features are more reliable at higher tumour fractions. Combined, they should be complementary.

#### Model 1 (Fragmentomics) vs Model 2 (Methylation) Results
```
Generating dataset ...
Extracting features ...

=========================================
Training Model 1: Fragmentomics only ...

=========================================
Model: Model 1 - Fragmentomics only
Features: 6
Samples: 1800 (1500 cancer, 300 healthy)
ROC AUC: 0.7584

Sensitivity by tumor fraction:
  TF=0.001:     0.387
  TF=0.005:     0.497
  TF=0.01:      0.597
  TF=0.05:      0.947
  TF=0.1:       1.000

Top features by importance:
  fragment_length_entropy:      0.3439
  short_fragment_ratio:         0.2625
  short_to_long_ratio:          0.1945
  nucleosomal_peak_ratio:       0.0932
  long_fragment_ratio:          0.0721
  median_fragment_length:       0.0339
Training Model 2: Methylation only ...

=========================================
Model: Model 2 - Methylation only
Features: 5
Samples: 1800 (1500 cancer, 300 healthy)
ROC AUC: 0.9307

Sensitivity by tumor fraction:
  TF=0.001:     0.393
  TF=0.005:     0.940
  TF=0.01:      0.987
  TF=0.05:      1.000
  TF=0.1:       1.000

Top features by importance:
  bimodality_score:     0.3844
  methylation_variance:         0.3356
  hypermethylated_fraction:     0.1568
  mean_methylation:     0.1115
  methylation_entropy:          0.0116

=========================================
SUMMARY COMPARISON
=========================================
Model                                  AUC
=========================================
Model 1 - Fragmentomics only        0.7584
Model 2 - Methylation only          0.9307

Sensitivity comparison by tumor fraction:
TF                M1        M2
-----------------------------------------
0.0010         0.387     0.393
0.0050         0.497     0.940
0.0100         0.597     0.987
0.0500         0.947     1.000
0.1000         1.000     1.000
```
- Both models still not performing well for TF = 0.0010
- "Model 2 - Methylation only" significantly outperforms "Model 1 - Fragmentomics only" for fractions 0.0050 and above. **A significant improvement!** 
#### Model 3: Fragmentomics + Methylation combined results
```
=========================================
Model: Model 3 — Combined
Features: 11
Samples: 1800 (1500 cancer, 300 healthy)
ROC AUC: 0.9345

Sensitivity by tumor fraction:
  TF=0.001:     0.397
  TF=0.005:     0.940
  TF=0.01:      0.987
  TF=0.05:      1.000
  TF=0.1:       1.000

Top features by importance:
  bimodality_score:     0.3147
  methylation_variance:         0.2617
  hypermethylated_fraction:     0.2329
  mean_methylation:     0.0942
  methylation_entropy:          0.0466
  fragment_length_entropy:      0.0163
  short_fragment_ratio:         0.0113
  short_to_long_ratio:          0.0095
  nucleosomal_peak_ratio:       0.0066
  long_fragment_ratio:          0.0049
  median_fragment_length:       0.0013

=========================================
SUMMARY COMPARISON
=========================================
Model                                  AUC
=========================================
Model 1 - Fragmentomics only        0.7584
Model 2 - Methylation only          0.9307
Model 3 — Combined                  0.9345

Sensitivity comparison by tumor fraction:
TF                M1        M2        M3
-----------------------------------------
0.0010         0.387     0.393     0.397
0.0050         0.497     0.940     0.940
0.0100         0.597     0.987     0.987
0.0500         0.947     1.000     1.000
0.1000         1.000     1.000     1.000
```
- M3 (combined) outperforms M2 only slightly for TF = 0.0010.
- M2 and M3 perform equally for TF 0.0050 and above.
- M3 does not significantly improve the classification sensitivity

**N_CPG_SITES increased to 1000 # was 500**
```
Generating dataset ...
Extracting features ...

=========================================
Training Model 1: Fragmentomics only ...

=========================================
Model: Model 1 - Fragmentomics only
Features: 6
Samples: 1800 (1500 cancer, 300 healthy)
ROC AUC: 0.7264

Sensitivity by tumor fraction:
  TF=0.001:     0.357
  TF=0.005:     0.403
  TF=0.01:      0.527
  TF=0.05:      0.930
  TF=0.1:       0.997

Top features by importance:
  fragment_length_entropy:      0.3075
  short_fragment_ratio:         0.2498
  short_to_long_ratio:          0.2408
  nucleosomal_peak_ratio:       0.0989
  long_fragment_ratio:          0.0686
  median_fragment_length:       0.0345
Training Model 2: Methylation only ...

=========================================
Model: Model 2 - Methylation only
Features: 5
Samples: 1800 (1500 cancer, 300 healthy)
ROC AUC: 0.9637

Sensitivity by tumor fraction:
  TF=0.001:     0.680
  TF=0.005:     0.990
  TF=0.01:      1.000
  TF=0.05:      1.000
  TF=0.1:       1.000

Top features by importance:
  bimodality_score:     0.4412
  methylation_variance:         0.2784
  hypermethylated_fraction:     0.1693
  mean_methylation:     0.1046
  methylation_entropy:          0.0064
Training Model 3: Fragmentomics & Methylation combined ...

=========================================
Model: Model 3 — Combined
Features: 11
Samples: 1800 (1500 cancer, 300 healthy)
ROC AUC: 0.9640

Sensitivity by tumor fraction:
  TF=0.001:     0.673
  TF=0.005:     0.990
  TF=0.01:      1.000
  TF=0.05:      1.000
  TF=0.1:       1.000

Top features by importance:
  bimodality_score:     0.3523
  methylation_variance:         0.2438
  hypermethylated_fraction:     0.2377
  mean_methylation:     0.0933
  methylation_entropy:          0.0464
  short_fragment_ratio:         0.0078
  short_to_long_ratio:          0.0071
  fragment_length_entropy:      0.0064
  nucleosomal_peak_ratio:       0.0025
  long_fragment_ratio:          0.0020
  median_fragment_length:       0.0005

=========================================
SUMMARY COMPARISON
=========================================
Model                                  AUC
=========================================
Model 1 - Fragmentomics only        0.7264
Model 2 - Methylation only          0.9637
Model 3 — Combined                  0.9640

Sensitivity comparison by tumor fraction:
TF                M1        M2        M3
-----------------------------------------
0.0010         0.357     0.680     0.673
0.0050         0.403     0.990     0.990
0.0100         0.527     1.000     1.000
0.0500         0.930     1.000     1.000
0.1000         0.997     1.000     1.000
```
- Significant improvement over previous results. M3 still doesn't significantly differ from M2.
