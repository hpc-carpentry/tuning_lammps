import sys, re
import numpy as np
import pandas as pd
import lammps_extract
import matplotlib.pyplot as plt
import math

def round_up(n):
    multiplier = 10 ** -1
    return math.ceil(n * multiplier)/multiplier

def cpu_v_gpu(data):
    # check if correct data is as input

    cpu_gpu_df = pd.DataFrame()
    group = data.groupby(data['Configuration'])
    cpu = group.get_group("CPU")
    gpu = group.get_group("GPU")
    gpu = gpu.reset_index()
    kkgpu = group.get_group("Kokkos/GPU")
    kkgpu = kkgpu.reset_index()

    #speed_up = pd.DataFrame
    cpu_gpu_df['# nodes'] = cpu['# nodes']
    cpu_gpu_df['# CPU Performance'] = cpu['Performance']
    cpu_gpu_df['# GPU Performance'] = gpu['Performance']
    cpu_gpu_df['# Kokkos/GPU Performance'] = kkgpu['Performance']
    speed_up_gpu = gpu['Performance']/cpu['Performance']
    speed_up_kkgpu = kkgpu['Performance']/cpu['Performance']
    #print(speed_up_gpu, speed_up_kkgpu)
    # cpu_gpu_df = pd.DataFrame()
    #print(math.ceil(max(data['Performance'])))

    fig, ax1 = plt.subplots(figsize=(8,6))
    ax1.plot(cpu['# nodes'], cpu['Performance'], 'bo-', label="CPU", linewidth=1.5, markersize=5)
    ax1.plot(gpu['# nodes'], gpu['Performance'], 'gv-', label="GPU Package", linewidth=1.5, markersize=7.5)
    ax1.plot(kkgpu['# nodes'], kkgpu['Performance'], 'r*-', label="Kokkos/GPU Package", linewidth=1.5, markersize=7.5)
    ax1.set_ylim(0, (round_up(max(data['Performance'])+1)))
    ax1.grid(color='k', linestyle='--', linewidth=1, alpha=0.2)
    ax1.set_xlim(1, (max(cpu['# nodes'])+0.01))
    ax1.set_xlabel("Number of nodes", fontsize=12, fontname="Arial")
    ax1.set_ylabel("Performance (timesteps/second)", fontsize=12, fontname="Arial")

    ax2 = ax1.twinx()
    #print(len(gpu['Performance']), len(cpu['# nodes']))
    ax2.plot(cpu['# nodes'], speed_up_gpu, 'gv', linestyle="dashed", label="Speed-up for GPU Package", linewidth=1.5, markersize=7.5)
    ax2.plot(cpu['# nodes'], speed_up_kkgpu, 'r*', linestyle="dashed", label="Speed-up for Kokkos/GPU Package", linewidth=1.5, markersize=7.5)
    ax2.set_ylabel("Speed up factor", fontsize=12, fontname="Arial")
    ax2.set_ylim(0,10)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc=2, ncol=1)
    fig.suptitle("11 million atom Lennard-Jones system, Intel Xeon E5-2680 v3 Haswell CPU 2x12 cores \n w. 4 K80 GPUs/nodes and Mellanox EDR InfiniBand network.\nLAMMPS 3Mar20, Intel Compiler and CUDA", fontsize=10)

    fig.savefig("CPU_v_GPU.png")

def gpu_perf(data):

    # new pd.DataFrame created to avoid SettingWithCopyWarning
    gpu_df = pd.DataFrame()
    data = data.sort_values(['# atoms', '# MPI tasks'])
    data = data.reset_index()
    group = data.groupby(data['# atoms'])
    _4K = group.get_group(4000)
    del _4K['index']
    _256K = group.get_group(256000)
    _256K = _256K.reset_index()
    del _256K['index']
    _11M = group.get_group(10976000)
    _11M = _11M.reset_index()
    del _11M['index']

    lengths = [len(_4K), len(_256K), len(_11M)]
    # checks that there are equal number of input gpu files per # atoms
    if all(i == lengths[0] for i in lengths) == False:
        raise Exception("Number of input GPU files do not match for normalisation plot.")

    gpu_df['4K MPI tasks'] = _4K['# MPI tasks']
    gpu_df['4K Performance'] = _4K['Performance']
    gpu_df['4K Normalised'] = gpu_df['4K Performance']/gpu_df['4K Performance'].max()
    
    gpu_df['256K MPI tasks'] = _256K['# MPI tasks']
    gpu_df['256K Performance'] = _256K['Performance']
    gpu_df['256K Normalised'] = gpu_df['256K Performance']/gpu_df['256K Performance'].max()

    gpu_df['11M MPI tasks'] = _11M['# MPI tasks']
    gpu_df['11M Performance'] = _11M['Performance']
    gpu_df['11M Normalised'] = gpu_df['11M Performance']/gpu_df['11M Performance'].max()

    fig, ax = plt.subplots()

    x_ticks = []
    num_gpu = 4
    for i in _4K['# MPI tasks']: 
        string = str(num_gpu) + "gpu" + str(i) + "proc"
        x_ticks.append(string)

    ax.plot(gpu_df['4K MPI tasks'], gpu_df['4K Normalised'], 'bo-', label="4K atoms", linewidth=0.75, markersize=5)
    ax.plot(gpu_df['256K MPI tasks'], gpu_df['256K Normalised'], 'gv-', label="256K atoms", linewidth=0.75, markersize=5)      
    ax.plot(gpu_df['11M MPI tasks'], gpu_df['11M Normalised'], 'r*-', label="11M atoms", linewidth=0.75, markersize=5)  
    
    ax.set_xticks(gpu_df['4K MPI tasks'])
    ax.set_xlabel("Number of cores", fontsize=12, fontname="Arial")
    ax.set_ylabel("Normalised speed-up factor per node", fontsize=12, fontname="Arial")

    ax.legend()
    ax.set_xticklabels(x_ticks)
    ax.grid(color='k', linestyle='--', linewidth=1, alpha=0.2)

    fig.suptitle("Lennard-Jones system in Intel Xeon E5-2680 v3 Haswell CPU 2x12 Cores \n w. x4 NVIDEA K80 GPUs/node, Malleanox EDR InfiniBand network. \n LAMMPS 3Mar20, Intel compiler and CUDA", fontsize=10)
    fig.savefig("GPU_performance.png")    

def scaling_rhodopsin(data):
    if data['Configuration'].str.contains("CPU").any():
        raise Exception("This contains LJ input files. Provide Rhodopsin input files.")
    if data['Configuration'].str.contains("GPU").any():
        raise Exception("This contains LJ input files. Provide Rhodopsin input files.")
    if data['Configuration'].str.contains("Kokkos/GPU").any():
        raise Exception("This contains LJ input files. Provide Rhodopsin input files.")
    
    scaling = pd.DataFrame()

    scaling_str = []
    for col in data.columns:
        if col == "Performance":
            break
        scaling_str.append(col)
    
    for s in scaling_str:
        scaling['Sp_'+s] = data[s][0]/data[s]
    scaling['MPI tasks'] = data['# MPI tasks']

    fig, ax = plt.subplots()

    ax.plot(scaling['MPI tasks'], scaling['Sp_Pair'], color='tab:blue', linestyle='-', marker='v', label='Pair', linewidth=1.25, markersize=2)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Bond    '], color='tab:green', linestyle='-', marker='v', label='Bond', linewidth=1.25, markersize=2)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Kspace '], color='tab:orange', linestyle='-', marker='v', label='Kspace', linewidth=1.25, markersize=2)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Neigh '], color='tab:red', linestyle='-', marker='v', label='Neigh', linewidth=1.25, markersize=2)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Comm'], color='tab:cyan', linestyle='-', marker='v', label='Comm', linewidth=1.25, markersize=2)
    #ax.plot(scaling['MPI tasks'], scaling['Sp_Output'], 'yo:', label='Output', linewidth=0.75, markersize=5)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Modify'], color='tab:olive', linestyle='-', marker='v', label='Modify', linewidth=1.25, markersize=2)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Other'], color='darkorchid', linestyle='-', marker='v', label='Other', linewidth=1.25, markersize=2)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Wall'], 'ko', linestyle='dashed', label='Walltime', linewidth=1, markersize=4)

    ax.set_xlabel("Number of cores", fontsize=12, fontname="Arial")
    ax.set_ylabel("Speed-up factor", fontsize=12, fontname="Arial")
    ax.set_xlim(0,400)
    ax.set_ylim(0,400)
    plt.legend()
    ax.grid(color='k', linestyle='--', linewidth=1, alpha=0.2)

    fig.suptitle("Speed-up factor for Rhodopsin system of 32K atoms", fontsize=12, y=0.92)
    fig.savefig("Rhodopsin_scaling.png") 

    #print(scaling)

def omp_pe_rhodopsin(data, serial_run=7019):
    #print(data, serial_run)
    rhodo_pe_df = pd.DataFrame()

    fig, ax = plt.subplots()

    #data.to_csv('file.csv')
    group = data.groupby(data['Configuration'])

    #if "MPI" in data['Configuration'].values:
    mpi_group = group.get_group("MPI")
    mpi_group = mpi_group[(mpi_group['# MPI tasks'] % 40 == 0)]
    mpi_group = mpi_group.reset_index()
    rhodo_pe_df['Nodes'] = mpi_group['# nodes']
    rhodo_pe_df['MPI_only_pe'] = (1.0/mpi_group['# nodes']/40)*(serial_run/mpi_group['Wall']*100)

    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['MPI_only_pe'], 'ko-', label='MPI-only', linewidth=3, markersize=4)

    #print(rhodo_pe_df)

    #if "OMP" in data['Configuration'].values:
    omp_group = group.get_group("OMP")
    omp_group = omp_group.sort_values(['# OMP threads', '# nodes'])
    omp_group = omp_group.reset_index()

    nums = [1, 2, 4, 5, 8, 10, 20, 40]
    rev_nums = nums[::-1]

    omp = omp_group.groupby("# OMP threads")
    for i in range(0, len(nums)):
        globals()['omp%s' % nums[i]] = omp.get_group(nums[i])
        globals()['omp%s' % nums[i]] = globals()['omp%s' % nums[i]].reset_index()
        del globals()['omp%s' % nums[i]]['index']
        del globals()['omp%s' % nums[i]]['level_0']
        rhodo_pe_df[str('%s_MPI_' % rev_nums[i])+str(nums[i])+'_OMP_pe'] = (1.0/globals()['omp%s' % nums[i]]['# nodes']/40)*(serial_run/globals()['omp%s' % nums[i]]['Wall']*100)

    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['1_MPI_40_OMP_pe'], color='tab:blue', linestyle='-', marker='o', label='1 MPI x 40 OpenMP', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['2_MPI_20_OMP_pe'], color='tab:green', linestyle='-', marker='v', label='2 MPI x 20 OpenMP', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['4_MPI_10_OMP_pe'], color='tab:orange', linestyle='-', marker='^', label='4 MPI x 10 OpenMP', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['5_MPI_8_OMP_pe'], color='tab:red', linestyle='-', marker='>', label='5 MPI x 8 OpenMP', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['8_MPI_5_OMP_pe'], color='tab:cyan', linestyle='-', marker='<', label='8 MPI x 5 OpenMP', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['10_MPI_4_OMP_pe'], color='tab:olive', linestyle='-', marker='*', label='10 MPI x 4 OpenMP', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['20_MPI_2_OMP_pe'], color='darkorchid', linestyle='-', marker='X', label='20 MPI x 2 OpenMP', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['40_MPI_1_OMP_pe'], color='peru', linestyle='-', marker='D', label='40 MPI x 1 OpenMP', linewidth=1.25, markersize=4)
    ax.grid(color='k', linestyle='--', linewidth=1, alpha=0.2)
    ax.set_ylim(0,100)
    ax.set_xlim(0.5,(rhodo_pe_df['Nodes'].max()+0.5))
    ax.legend(ncol=2, loc=1, fontsize=8)
    ax.set_xlabel("Number of nodes", fontsize=12, fontname="Arial")
    ax.set_ylabel("Parallel efficiency (%)", fontsize=12, fontname="Arial")
    fig.suptitle("Intel Xeon Gold (Skylake) processors with 2x20-core 2.4 GHz,\n192 GB RAM Rhodopsin system (32K atoms), lj/charmm/coul/long\n+ PPPM with USER-OMP (Intel compiler 2019u5, GCC 8.2.0)", fontsize=11, y=0.99)
    fig.savefig("Rhodopsin_omp_pe.png") 


def kokkos_omp_pe_rhodopsin(data, serial_run=7019):
    #if "Kokkos/OMP" in data['Configuration'].values:

    rhodo_pe_df = pd.DataFrame()

    fig, ax = plt.subplots()

    #data.to_csv('file.csv')
    group = data.groupby(data['Configuration'])

    #if "MPI" in data['Configuration'].values:
    mpi_group = group.get_group("MPI")
    mpi_group = mpi_group[(mpi_group['# MPI tasks'] % 40 == 0)]
    mpi_group = mpi_group.reset_index()
    rhodo_pe_df['Nodes'] = mpi_group['# nodes']
    rhodo_pe_df['MPI_only_pe'] = (1.0/mpi_group['# nodes']/40)*(serial_run/mpi_group['Wall']*100)

    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['MPI_only_pe'], 'ko-', label='MPI-only', linewidth=3, markersize=4)

    #print(kkomp_group)
    kkomp_group = group.get_group("Kokkos/OMP")
    kkomp_group = kkomp_group.sort_values(['# OMP threads', '# nodes'])
    kkomp_group = kkomp_group.reset_index()

    kkomp = kkomp_group.groupby("# OMP threads")
    
    nums = [1, 2, 4, 5, 8, 10, 20, 40]
    rev_nums = nums[::-1] 

    for i in range(0, len(nums)):
        globals()['omp%s' % nums[i]] = kkomp.get_group(nums[i])
        globals()['omp%s' % nums[i]] = globals()['omp%s' % nums[i]].reset_index()
        del globals()['omp%s' % nums[i]]['index']
        del globals()['omp%s' % nums[i]]['level_0']
        rhodo_pe_df[str('%s_MPI_' % rev_nums[i])+str(nums[i])+'_OMP_Kokkos_pe'] = (1.0/globals()['omp%s' % nums[i]]['# nodes']/40)*(serial_run/globals()['omp%s' % nums[i]]['Wall']*100)

    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['1_MPI_40_OMP_Kokkos_pe'], color='tab:blue', linestyle='-', marker='o', label='1 MPI x 40 OpenMP w. Kokkos', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['2_MPI_20_OMP_Kokkos_pe'], color='tab:green', linestyle='-', marker='v', label='2 MPI x 20 OpenMP w. Kokkos', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['4_MPI_10_OMP_Kokkos_pe'], color='tab:orange', linestyle='-', marker='^', label='4 MPI x 10 OpenMP w. Kokkos', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['5_MPI_8_OMP_Kokkos_pe'], color='tab:red', linestyle='-', marker='>', label='5 MPI x 8 OpenMP w. Kokkos', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['8_MPI_5_OMP_Kokkos_pe'], color='tab:cyan', linestyle='-', marker='<', label='8 MPI x 5 OpenMP w. Kokkos', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['10_MPI_4_OMP_Kokkos_pe'], color='tab:olive', linestyle='-', marker='*', label='10 MPI x 4 OpenMP w. Kokkos', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['20_MPI_2_OMP_Kokkos_pe'], color='darkorchid', linestyle='-', marker='X', label='20 MPI x 2 OpenMP w. Kokkos', linewidth=1.25, markersize=4)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['40_MPI_1_OMP_Kokkos_pe'], color='peru', linestyle='-', marker='D', label='40 MPI x 1 OpenMP w. Kokkos', linewidth=1.25, markersize=4)
    ax.grid(color='k', linestyle='--', linewidth=1, alpha=0.2)
    ax.set_ylim(0,100)
    ax.set_xlim(0.5,(rhodo_pe_df['Nodes'].max()+0.5))
    ax.legend(ncol=2, loc=1, fontsize=8)
    ax.set_xlabel("Number of nodes", fontsize=12, fontname="Arial")
    ax.set_ylabel("Parallel efficiency (%)", fontsize=12, fontname="Arial")
    fig.suptitle("Intel Xeon Gold (Skylake) processors with 2x20-core 2.4 GHz,\n192 GB RAM Rhodopsin system (32K atoms), lj/charmm/coul/long\n+ PPPM with USER-OMP and Kokkos (Intel compiler 2019u5, GCC 8.2.0)", fontsize=11, y=0.99)

    fig.savefig("Rhodopsin_kokkos_omp.png") 

if __name__ == "__main__":
    #extract_data(sys.argv[1:])
    lammps_data = lammps_extract.extract_data(sys.argv[1:])

    #print(lammps_data)
    
    #cpu_v_gpu(lammps_data)
    
    #gpu_perf(lammps_data)
    
    #scaling_rhodopsin(lammps_data)

    omp_pe_rhodopsin(lammps_data)
    kokkos_omp_pe_rhodopsin(lammps_data)
    
    #print(log_lammps)