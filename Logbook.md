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

==================================================
Model: Model 1 - Fragmentomics Only
Features: 6
Samples: 1800 (1500 cancer, 300 healthy)
ROC AUC: 0.7505

Sensitivity by tumor fraction:
  TF=0.001: 0.343
  TF=0.005: 0.473
  TF=0.01: 0.600
  TF=0.05: 0.940
  TF=0.1: 0.997

Top features by importance:
  fragment_length_entropy: 0.3325
  short_fragment_ratio: 0.2610
  short_to_long_ratio: 0.2065
  nucleosomal_peak_ratio: 0.0867
  long_fragment_ratio: 0.0705
  median_fragment_length: 0.0427

Final AUC: 0.750460
```
