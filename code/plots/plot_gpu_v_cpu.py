import sys, re
import numpy as np
import pandas as pd
import lammps_extract
from lammps_plot import cpu_v_gpu
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    #extract_data(sys.argv[1:])
    lammps_data = lammps_extract.extract_data(sys.argv[1:])
    cpu_v_gpu(lammps_data)