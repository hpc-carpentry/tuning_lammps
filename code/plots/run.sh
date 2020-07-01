#!/bin/bash

# Input paths for files
gpu_performance_L=/Users/chris/Documents/Courses/Random Tests/LAMMPS/out_files_gpu/gpu_perf/LARGE/*
gpu_performance_M=/Users/chris/Documents/Courses/Random Tests/LAMMPS/out_files_gpu/gpu_perf/MEDIUM/*
gpu_performance_S=/Users/chris/Documents/Courses/Random \Tests/LAMMPS/out_files_gpu/gpu_perf/SMALL/*
gpu_v_cpu=0
scaling=0
omp_pe=0
kokkos_omp_pe=0

python plot_gpu_perf.py ${gpu_performance_L} ${gpu_performance_M} ${gpu_performance_S}
