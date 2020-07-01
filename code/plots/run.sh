#!/bin/bash

D=/Users/chris/Documents/Courses/Random_Tests/LAMMPS/out_files_
# Input paths for files
gpu_performance_L=${D}gpu/gpu_perf/LARGE/*
gpu_performance_M=${D}gpu/gpu_perf/MEDIUM/*
gpu_performance_S=${D}gpu/gpu_perf/SMALL/*

gpu_v_cpu_cpu=${D}basic/*lammps
gpu_v_cpu_gpu=${D}gpu/*lammps
gpu_v_cpu_kkgpu=${D}kkgpu/*lammps

scaling=${D}no_opt/32K/*
omp_pe=${D}user_omp/*
kkomp_pe=${D}kkomp/*

#python plot_gpu_perf.py ${gpu_performance_L} ${gpu_performance_M} ${gpu_performance_S}
#python plot_gpu_v_cpu.py ${gpu_v_cpu_cpu} ${gpu_v_cpu_gpu} ${gpu_v_cpu_kkgpu}
#python plot_scaling_rhodopsin.py ${scaling}
python plot_omp_pe_rhodopsin.py ${scaling} ${omp_pe}
python plot_kokkos_omp_pe_rhodopsin.py ${scaling} ${kkomp_pe}
