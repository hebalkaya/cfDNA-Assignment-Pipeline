# General notes
These are the notes I am taking along the way. Some as a refresher and others as new information.

## Review

`SNVs`: **Single Nucleotide Variations**: Single Nucleotide Variants (SNVs) and Single Nucleotide Polymorphisms (SNPs) both describe single-base pair changes in DNA, but the key distinction is population frequency. SNVs are any single-base change found in a sample (including rare or somatic mutations), whereas SNPs are common, stable variants found in >1% of a population.

`CNAs`: **Copy number alterations**: a type of genomic structural variation where the number of copies of a specific DNA segment varies from the standard diploid (two copies) state. These changes, including deletions and amplifications, are a hallmark of cancer and congenital diseases, driving tumor progression, therapeutic resistance, and disease risk.

`cfDNA`: **Cell-free DNA**: refers to degraded DNA fragments, typically ~165bp, circulating freely in blood plasma, urine, and other body fluids, largely released via apoptosis or necrosis.

`fragmentomics`: The study of cell-free DNA (cfDNA) fragmentation patterns in blood to detect diseases like cancer. By analyzing features like fragment size, end motifs, and nucleosome positioning, it acts as a non-invasive liquid biopsy to identify tumor presence, tissue-of-origin, and progression without needing prior mutation knowledge.

>Fragmentomics is powerful because tumour-derived cfDNA has a distinct fragmentation pattern compared to healthy cfDNA
>Specifically, tumour cfDNA tends to have shorter fragments and different nucleosomal positioning signatures.

## On the models
### CyclomicsSeq
Targeted TP53 mutation detection, consensus calling, validated clinically
### NanoRCS
The bewest platform (published Genome Research, March 2025)

Genome-wide consensus sequencing detecting SNVs + copy number alterations + fragmentomics simultaneously, all from one blood draw

Detects tumor fractions as low as 0.24%
