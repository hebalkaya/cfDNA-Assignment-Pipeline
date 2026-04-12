# General notes
These are the notes I am taking along the way. Some as a refresher and others as new information.

## Review

`SNVs`: **Single Nucleotide Variations**: Single Nucleotide Variants (SNVs) and Single Nucleotide Polymorphisms (SNPs) both describe single-base pair changes in DNA, but the key distinction is population frequency. SNVs are any single-base change found in a sample (including rare or somatic mutations), whereas SNPs are common, stable variants found in >1% of a population.

`CNAs`: **Copy number alterations**: a type of genomic structural variation where the number of copies of a specific DNA segment varies from the standard diploid (two copies) state. These changes, including deletions and amplifications, are a hallmark of cancer and congenital diseases, driving tumor progression, therapeutic resistance, and disease risk.

`cfDNA`: **Cell-free DNA**: refers to degraded DNA fragments, typically ~165bp, circulating freely in blood plasma, urine, and other body fluids, largely released via apoptosis or necrosis.

`fragmentomics`: The study of cell-free DNA (cfDNA) fragmentation patterns in blood to detect diseases like cancer. By analyzing features like fragment size, end motifs, and nucleosome positioning, it acts as a non-invasive liquid biopsy to identify tumor presence, tissue-of-origin, and progression without needing prior mutation knowledge.

>Fragmentomics is powerful because tumour-derived cfDNA has a distinct fragmentation pattern compared to healthy cfDNA
>Specifically, tumour cfDNA tends to have shorter fragments and different nucleosomal positioning signatures.

## Methylation
### The Basics
Methylation is an epigenetic process. Meaning it modifies how genes behave without changing the underlying DNA sequence itself. Specifically, it involves the addition of a methyl group (CH₃) to a cytosine base in DNA, typically at sites called CpG dinucleotides (where cytosine is followed by guanine).
Think of it like a set of sticky notes on a book: the words (DNA sequence) don't change, but the notes tell the reader which chapters to pay attention to and which to skip. Methylation generally silences gene expression. Methylated genes tend to be switched off.
In healthy cells, methylation patterns are tightly regulated and predictable. They vary by tissue type and serve important roles in development, cell identity, and gene regulation.

[!Metylation](https://blog.lgcclinicaldiagnostics.com/hs-fs/hubfs/0.%20Blogs/NGS%20Blog/DNA%20Methyltransferases.png)

### Hypermethylation & What Goes Wrong in Cancer
Hypermethylation refers to an excess of methylation at a region that is normally unmethylated or lightly methylated. In cancer, this frequently occurs at the promoter regions of tumor suppressor genes. The very genes whose job is to slow or stop uncontrolled cell growth.
When a tumor suppressor gene's promoter becomes hypermethylated, the gene gets silenced. Without that brake on cell proliferation, cancerous growth can take hold. This is a hallmark of many cancers and can be detected before a tumor is large enough to show up on a scan. Importantly, different cancer types tend to have distinctive hypermethylation signatures, which makes methylation patterns potentially useful as a cancer fingerprint.

## On the tools
### CyclomicsSeq
* Targeted TP53 mutation detection, consensus calling, validated clinically
### Epinn
* PCR-free multi-omics: simultaneous mutation + methylation detection without chemical treatment
### NanoRCS
* The bewest platform (published Genome Research, March 2025)
* Genome-wide consensus sequencing detecting SNVs + copy number alterations + fragmentomics simultaneously, all from one blood draw
* Detects tumor fractions as low as 0.24%
