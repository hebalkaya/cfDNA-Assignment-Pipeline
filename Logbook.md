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
- [ ] Complete classifier model 1: Random Forest on Fragmentomics
