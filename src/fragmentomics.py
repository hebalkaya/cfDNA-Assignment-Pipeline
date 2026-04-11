"""
Extracts fragment length features from cfDNA samples.

Biological basis:
    Healthy cfDNA is predominantyl nucleosomal (~167bp), reflecting
    orderly apoptotic cleavage between nucleosomes. Tumor-derived cfDNA (ctDNA)
    shows enrichment of shorter sub-nucleosomal fragments (~143bp) due to altered
    chromatin structure in cancer cells.

    These differences in fragment length distribution provide a tumor-fraction-dependent
    signal detectable from sequencing data.

Source papers:
    * Underhill et al. 2016, PLOS (Mouse cfDNA & ctDNA fragment lengths) (Fragment Length of Circulating Tumor DNA)
    * Snyder et al. 2016, Cell (cfDNA fragment lengths) (Cell-free DNA Comprises an In Vivo Nucleosome Footprint that Informs Its Tissues-Of-Origin)
    * Cristiano et al., Nature 2019 (Genome-wide cell-free DNA fragmentation in patients with cancer)
"""