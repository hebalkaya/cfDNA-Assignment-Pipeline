# Google Compute Engine Virtual Machine Setup
## Authenticate Google Cloud CLI
```
gcloud auth login
gcloud config set project cfdna-pipeline-492919
```
## Build and push Docker image to Google Cloud
```
# Configure Docker to use gcloud credentials
gcloud auth configure-docker

# Build the image
docker build -t gcr.io/cfdna-pipeline-492919/cfdna-pipeline:v1 .

# Push to Google Container Registry
docker push gcr.io/cfdna-pipeline-492919/cfdna-pipeline:v1
```
## Create Google Cloud Storage bucket for results
```
gsutil mb -l europe-west4 gs://cfdna-pipeline-results-heb
```
## Create and SSH into a Virtual Machine
```
gcloud compute instances create cfdna-pipeline-vm \
  --zone=europe-west4-a \
  --machine-type=e2-standard-2 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --scopes=cloud-platform

# SSH in
gcloud compute ssh cfdna-pipeline-vm --zone=europe-west4-a
```
## Run pipeline on the Virtual Machine
```
# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker

# Authenticate with GCR
gcloud auth configure-docker

# Pull and run docker image
docker pull gcr.io/cfdna-pipeline-492919/cfdna-pipeline:v1
docker run gcr.io/cfdna-pipeline-492919/cfdna-pipeline:v1
```
## Success criteria: Output
```
hebalkaya at mac in ~/cfDNA-Assignment-Pipeline on main % gcloud compute ssh cfdna-pipeline-vm --zone=europe-west4-a
hebalkaya@cfdna-pipeline-vm:~$ docker run gcr.io/cfdna-pipeline-492919/cfdna-pipeline:v1
========================================
cfDNA Multi-Signal Cancer Detection
========================================
[1/4] Simulating cfDNA dataset
* 900 samples | * 6 tumor fractions
[2/4] Extracting fragmentomics features fragmentomics + 5 methylation features
[3/4] Training classifiers ...
```
