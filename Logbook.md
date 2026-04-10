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
