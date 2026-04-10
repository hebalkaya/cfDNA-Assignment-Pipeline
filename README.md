# cfDNA Assignment Pipeline
Initiated on April 10, 2026 to showcase a bioinformatician's relevant abilities in an interview.

## Over the Idea
Tumour-derived cfDNA differs from healthy cfDNA in two independent ways: how it's fragmented and how it's methylated. By building a pipeline that extracts and combines both signals, we can detect cancer at lower tumour fractions than either signal alone.

## On the Data
### Option A: Simulate with real parameters
Rather than pure simulation, parameterising the simulation from published real data. The exact fragment length distributions, methylation values, and tumour fractions are taken from published papers and used as ground truth parameters.

### Option B: Use the Cyclomics public GitHub data
Obtaining example data from the ```[Cyclomics GitHub repository]```(https://github.com/cyclomics). Real nanopore cfDNA data. Could be used as validation set as well as option C.

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


### Module 1 — Data simulation
Generating realistic cfDNA datasets with known tumour fractions (0%, 0.1%, 0.5%, 1%, 5%, 10%) by mixing:

Healthy cfDNA fragments: Gaussian distribution centred at 167bp
Tumour cfDNA fragments: shifted distribution with enrichment at 143bp and shorter fragments
Methylation profiles: tumour samples have hypermethylation at cancer-specific CpG islands
