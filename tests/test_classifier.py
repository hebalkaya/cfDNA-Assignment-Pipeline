"""Tests for classifier.py"""
import numpy as np
import pandas as pd
import pytest
from src.simulate import simulate_dataset
from src.fragmentomics import extract_fragmentomics_dataframe
from src.classifier import *