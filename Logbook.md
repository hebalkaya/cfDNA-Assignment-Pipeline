# Logbook
### Friday, April 10

#### Set up Google Cloud
- [X] Set up Google Cloud
- [X] Set up Google Cloud Project ```cfdna-pipeline``` (ID: cfdna-pipeline-492919)
- [X] Set up Google Cloud Data Bucket ```cfdna-results-he``` (Not publicly accessible)
- [X] Install gcloud CLI
> For various serverless products, the gcloud CLI is the primary interface by which you upload code to run and generally support your development workflow.
```
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz
```
```
tar -xf google-cloud-cli-darwin-arm.tar.gz
```
```
./google-cloud-sdk/install.sh
```
```
Welcome to the Google Cloud CLI!
Your current Google Cloud CLI version is: 564.0.0
```
- [X] Authenticate gcloud CLI
```
gcloud init
```
```
You are now authenticated with the gcloud CLI!
```
#### Authenticate Git
- [X] Initiate Git
- [X] Create SSH Key
- [X] Clone Git repo
```
git clone git@github.com:hebalkaya/cfDNA-Assignment-Pipeline.git
```
#### Build the complete structure
- [X] Build the skeleton

#### Begin coding
- [X] Initiated src/simulate.py
- [X] Initiated tests/test_simulate.py
- [X] Define data class SampleData
- [X] Complete simulate_fragment_lengths function within simulate.py
- [X] Complete test_fragment_lengths_within_bounds within test_simulate.py
- [X] Complete test_healthy_longer_than_tumor within test_simulate.py

#### Build Docker and run tests inside it
- [X] Build the Docker image
```
docker build -t cfdna-pipeline .
```
- [X] Run tests inside the container
```
docker compose run test
```
- [X] Pass the test: test_fragment_lengths_within_bounds
- [X] Pass the test: test_healthy_longer_than_tumor
