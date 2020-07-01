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

    fig, ax1 = plt.subplots()
    ax1.plot(cpu['# nodes'], cpu['Performance'], 'bo-', label="CPU Performance", linewidth=0.75, markersize=5)
    ax1.plot(gpu['# nodes'], gpu['Performance'], 'go-', label="GPU Performance", linewidth=0.75, markersize=5)
    ax1.plot(kkgpu['# nodes'], kkgpu['Performance'], 'ro-', label="Kokkos/GPU Performance", linewidth=0.75, markersize=5)
    ax1.set_ylim(0, (round_up(max(data['Performance'])+1)))
    ax1.grid(color='k', linestyle='--', linewidth=1, alpha=0.2)
    ax1.set_xlim(1, (max(cpu['# nodes'])+0.01))

    ax2 = ax1.twinx()
    #print(len(gpu['Performance']), len(cpu['# nodes']))
    ax2.plot(cpu['# nodes'], speed_up_gpu, 'gv:', label="GPU Performance", linewidth=0.75, markersize=5)
    ax2.plot(cpu['# nodes'], speed_up_kkgpu, 'rv:', label="Kokkos/GPU Performance", linewidth=0.75, markersize=5)
    ax2.set_ylim(0,10)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc=2, borderaxespad=0., ncol=2)

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
    ax.set_xticklabels(x_ticks)
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

    ax.plot(scaling['MPI tasks'], scaling['Sp_Pair'], 'bo-', label='Pair', linewidth=0.75, markersize=1)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Bond    '], 'go-', label='Bond', linewidth=0.75, markersize=1)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Kspace '], 'ro-', label='Kspace', linewidth=0.75, markersize=1)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Neigh '], 'co-', label='Neigh', linewidth=0.75, markersize=1)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Comm'], 'mo-', label='Comm', linewidth=0.75, markersize=1)
    #ax.plot(scaling['MPI tasks'], scaling['Sp_Output'], 'yo:', label='Output', linewidth=0.75, markersize=5)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Modify'], 'yo-', label='Modify', linewidth=0.75, markersize=1)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Other'], color='orange', linestyle='-', label='Other', linewidth=0.75, markersize=2)
    ax.plot(scaling['MPI tasks'], scaling['Sp_Wall'], 'ko:', label='Walltime', linewidth=0.75, markersize=4)
    plt.legend()
    ax.grid(color='k', linestyle='--', linewidth=1, alpha=0.2)
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

    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['MPI_only_pe'], 'bo-', label='MPI-only', linewidth=3, markersize=4)

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

    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['1_MPI_40_OMP_pe'], 'ko-', label='1 MPI x 40 OpenMP', linewidth=0.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['2_MPI_20_OMP_pe'], 'ko-', label='2 MPI x 20 OpenMP', linewidth=0.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['4_MPI_10_OMP_pe'], 'ko-', label='4 MPI x 10 OpenMP', linewidth=0.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['5_MPI_8_OMP_pe'], 'ko-', label='5 MPI x 8 OpenMP', linewidth=0.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['8_MPI_5_OMP_pe'], 'ko-', label='8 MPI x 5 OpenMP', linewidth=0.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['10_MPI_4_OMP_pe'], 'ko-', label='10 MPI x 4 OpenMP', linewidth=0.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['20_MPI_2_OMP_pe'], 'ko-', label='20 MPI x 2 OpenMP', linewidth=0.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['40_MPI_1_OMP_pe'], 'ko-', label='40 MPI x 1 OpenMP', linewidth=0.75, markersize=1)
    ax.grid(color='k', linestyle='--', linewidth=1, alpha=0.2)
    ax.set_ylim(0,100)
    ax.set_xlim(0.5,(rhodo_pe_df['Nodes'].max()+0.5))
    ax.legend()
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

    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['MPI_only_pe'], 'bo-', label='MPI-only', linewidth=3, markersize=4)

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

    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['1_MPI_40_OMP_Kokkos_pe'], 'go-', label='1 MPI x 40 OpenMP w. Kokkos', linewidth=2.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['2_MPI_20_OMP_Kokkos_pe'], 'r:', label='2 MPI x 20 OpenMP w. Kokkos', linewidth=2.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['4_MPI_10_OMP_Kokkos_pe'], 'r:', label='4 MPI x 10 OpenMP w. Kokkos', linewidth=2.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['5_MPI_8_OMP_Kokkos_pe'], 'r:', label='5 MPI x 8 OpenMP w. Kokkos', linewidth=2.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['8_MPI_5_OMP_Kokkos_pe'], 'r:', label='8 MPI x 5 OpenMP w. Kokkos', linewidth=2.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['10_MPI_4_OMP_Kokkos_pe'], 'r:', label='10 MPI x 4 OpenMP w. Kokkos', linewidth=2.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['20_MPI_2_OMP_Kokkos_pe'], 'r:', label='20 MPI x 2 OpenMP w. Kokkos', linewidth=2.75, markersize=1)
    ax.plot(rhodo_pe_df['Nodes'], rhodo_pe_df['40_MPI_1_OMP_Kokkos_pe'], 'r:', label='40 MPI x 1 OpenMP w. Kokkos', linewidth=2.75, markersize=1)

    ax.grid(color='k', linestyle='--', linewidth=1, alpha=0.2)
    ax.set_ylim(0,100)
    ax.set_xlim(0.5,(rhodo_pe_df['Nodes'].max()+0.5))
    ax.legend()
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