#!/bin/bash

# Input paths for 
gpu_performance_L="Enter path to large GPU run"
gpu_performance_M="Enter path to medium GPU run"
gpu_performance_S="Enter path to small GPU run"

gpu_v_cpu_cpu="Enter path to cpu LJ runs"
gpu_v_cpu_gpu="Enter path to gpu LJ runs"
gpu_v_cpu_kkgpu="Enter path to kokkos/gpu LJ runs"

scaling="Enter path to rhodopsin scaling"
omp_pe="Enter path to rhodopsin OpenMP runs"
kkomp_pe="Enter path to rhodopsin OpenMP Kokkos runs"

# Comment out commands not to be run
python plot_gpu_perf.py ${gpu_performance_L} ${gpu_performance_M} ${gpu_performance_S}
python plot_gpu_v_cpu.py ${gpu_v_cpu_cpu} ${gpu_v_cpu_gpu} ${gpu_v_cpu_kkgpu}
python plot_scaling_rhodopsin.py ${scaling}
python plot_omp_pe_rhodopsin.py ${scaling} ${omp_pe}
python plot_kokkos_omp_pe_rhodopsin.py ${scaling} ${kkomp_pe}