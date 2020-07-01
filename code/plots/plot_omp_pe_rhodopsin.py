import sys, re
import numpy as np
import pandas as pd
import lammps_extract
from lammps_plot import omp_pe_rhodopsin
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    #extract_data(sys.argv[1:])
    lammps_data = lammps_extract.extract_data(sys.argv[1:])
    omp_pe_rhodopsin(lammps_data)