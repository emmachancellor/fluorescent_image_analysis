import numpy as np
import matplotlib.pyplot as plt
import os
from cellpose import models
from cellpose.io import imread

# Load pre-trained model
model = models.CellposeModel(model_type='bladder_cancer')

# Path to files
folder_path = "labshare/LL07132018/New_tumor_coculture_data/SIY_hi_t_spot2"