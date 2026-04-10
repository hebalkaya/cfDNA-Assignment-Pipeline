"""
Generates synthetic cfDNA datasets with known tumor fractions.

Biological basis (from literature):
* Healthy cfDNA: fragment lengths ~167bp (nucleosomal peak, the length of DNA associated with a nucleosome plus linker)
* Tumour cfDNA: enriched ~143bp (sub-nucleosomal, altered chromatin)
* Cancer methylation: hypermetilation at tumour specific CpG islands

Parameters derived from / Source papers:
* Underhill et al. 2016, PLOS (mouse cfDNA & ctDNA fragment lengths) (Fragment Length of Circulating Tumor DNA)
* Snyder et al. 2016, Cell (cfDNA fragment lengths) (Cell-free DNA Comprises an In Vivo Nucleosome Footprint that Informs Its Tissues-Of-Origin)
* Hanahan & Weinberg 2011 (methylation as cancer hallmark)
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List