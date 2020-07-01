import sys
import numpy as np
import re
import pandas as pd

tags = ["Pair", "Bond    ", "Kspace ",  "Neigh ", "Comm", "Output", "Modify", "Other"]
output = []
mpi_breakdown = []
walltime = []
wall_out = []
perf_out = []
mpi_grid = []
node_config = []
mpi_omp = []
fin = []
nprocs_str = []
mpi_dat = pd.DataFrame()

# Function to extract the walltime from the log.lammps file
## NB: Used within the extract_data(files) function below.
def extract_walltime(arr_in, arr_out):
    arr_temp = []
    for i in arr_in:
        arr_temp.append(re.findall(': (.+)\n', i))
    for sublist in arr_temp:
        for item in sublist:
            h, m, s = item.split(':')
            secs = int(h) * 3600 + int(m) * 60 + int(s)
            arr_out.append(secs)

#def extract_core_count()


def extract_performance(arr_in, arr_out):
    arr_temp = []
    for i in range (0, len(arr_in)):
        split_str = arr_in[i].split(" ")
        arr_temp.append(split_str[-2])
    for item in arr_temp:
        arr_out.append(float(item))


def extract_MPI_breakdown(arr, tag):
    numbers, sorted_arr, arr_x = [], [], []
    for i in range(0, len(arr)):
        split_string = arr[i].split("|")
        numbers.append(split_string[2])
    arr_temp = np.array([num.strip() for num in numbers])
    arr_temp = arr_temp.astype(np.float)

    for i in range(0, len(arr_temp)):
        arr_x.append(arr_temp[i])

    tag_num = len(list(tag.values())[0])
    tag_name = list(tag.values())[0]
    
    for i in range(0, tag_num):
        sorted_arr.append(arr_x[i::tag_num])

    sorted_arr = np.around(sorted_arr, decimals = 5)
    
    dicts = {}

    for i in range(0, tag_num):
        dicts[tag_name[i]] = sorted_arr[i]
    
    return(dicts)

def extract_tasks_threads_nodes(in_loop, in_cpu, in_mpi_grid, in_sim):
    global omp_threads, mpi_tasks, num_nodes, num_atoms
    # Condition which removes duplicate entries of MPI config line
    if len(in_mpi_grid) != len(in_loop):
        in_mpi_grid = in_mpi_grid[0::2]

    
    other = []
    for arr in in_loop, in_cpu, in_mpi_grid:
        for item in arr:
            other.append([int(i) for i in item.split() if i.isdigit()])
    
    
    atom_temp = other[0:len(in_mpi_grid)]
    mpi_temp = other[-len(in_mpi_grid):]
    tasks_threads = other[len(in_mpi_grid):-len(in_mpi_grid)]

    mpi_tasks = [item[0] for item in tasks_threads]
    omp_threads = [item[1] for item in tasks_threads]
    num_atoms = [item[2] for item in atom_temp]

    ext_procs = other[:len(in_loop)]
    procs_temp = [item[0] for item in ext_procs]
    
    if in_sim == "LJ":
        arr_out = []

        for i in mpi_temp:
            result = np.prod(i)
            arr_out.append(result)

        # Condition which looks at GPU performance. COULD generate bug with number of nodes
        # in case of issue
        if all(i == num_atoms[0] for i in num_atoms) == True:
            num_nodes = arr_out/arr_out[0]      
            num_nodes = num_nodes.astype(int)   
        else:
            num_nodes = [1] * len(num_atoms)
            print("Warning: Assuming LJ system size GPU comparison. Ignore warning if this is expected.\n")
        
        
    elif in_sim == "Rhodopsin":

        if all(i == procs_temp[0] for i in procs_temp) == True:
            num_nodes = [40] * len(in_loop)
            #num_nodes = [min(mpi_tasks)] * len(in_loop)
            
        else:
            num_nodes = [i / 40 for i in procs_temp]

            for i in range(0, len(num_nodes)):
                if num_nodes[i] <= 1:
                    num_nodes[i] = 1
            for i in range(0, len(num_nodes)):
                num_nodes[i] = int(num_nodes[i])

        
    else:
        raise Exception("Unclear input. Check input files.")

###                                                     

def create_data(mpi_breakdown, walltime, performance, config, mpi, threads, nodes, atoms):
    df = pd.DataFrame(data=mpi_breakdown)
    df['Wall'] = walltime
    df['Performance'] = performance
    if len(config) == 0:
        config = []
    df['Configuration'] = config
    df['# MPI tasks'] = mpi
    df['# OMP threads'] = threads
    df['# nodes'] = nodes
    df['# atoms'] = atoms
    df = df.sort_values(['Configuration', '# nodes', '# MPI tasks'])
    df = df.reset_index()
    del df['index']
    return(df)


def extract_data(files):
    # Creates dictionary needed to ascertain files have the same MPI breakdowns
    sorter = dict()
    file_type = []
    # Section which searches files for tag occurrences
    for file_x in files:
        with open(file_x, 'r') as f:
            for line in f.readlines():
                for subs in tags:
                    if line.startswith(subs):
                        output.append(subs)
                
        output_1 = np.copy(output)
        output_1 = output_1.tolist()
        sorter[file_x] = output_1
        output.clear()
    
    # Condition to ensure the file input MPI fields are the same, otherwise it fails
    if (all(value == list(sorter.values())[0] for value in sorter.values())) == False:
        raise Exception("MPI timing breakdown field names between files do not match.")
    # Condition to ensure GPU, Kokkos GPU and normal files cannot be plotted together
    else:
        full_line, walltime, perf = [], [], []
        for file_x in files:
            with open(file_x, 'r') as fi:
                
                for line in fi:

                    """
                    Check simulation type
                    """

                    # Check simulation type
                    if line.startswith("# 3d Lennard-Jones melt"):
                        file_type.append("LJ")
                    if line.startswith("# Rhodopsin model"):
                        file_type.append("Rhodopsin")
                    
                    # is Kokkos enabled?
                    if line.startswith("KOKKOS mode is enabled"):
                        file_type.append("Kokkos")

                    # LJ GPU?
                    if "variable ngpu" in line:
                        file_type.append("GPU")

                    # Rhodopsin omp?
                    if "package omp 0" in line:
                        file_type.append("OMP")
                    
                    """
                    Extract file data
                    """
                    # Extract looptime, no. procs, no. atoms, 
                    if line.startswith("Loop time of"):
                        nprocs_str.append(line)

                    # Extracts the walltime data from file
                    if line.startswith('Total wall time: '):
                        walltime.append(line)

                    if "CPU use" in line:
                        mpi_omp.append(line)
                    
                    if "MPI processor grid" in line:
                        mpi_grid.append(line)
                    
                    # GPU files only
                    if "core grid within node" in line:
                        node_config.append(line)                      

                    if line.startswith('Performance'):
                        perf.append(line)
                    for i in tags:
                        if line.startswith(i):
                            full_line.append(line[:])
        
        config = []

        if "LJ" in file_type:
            sim_type = "LJ"
            file_type = np.array(file_type)
            x = file_type.reshape(int(len(file_type)/2),2)
            cpu_arr = ['LJ', 'LJ']
            gpu_arr = ['LJ', 'GPU']
            kok_gpu_arr = ['Kokkos', 'LJ']
            for i in range(0, len(x)):
                comp_cpu = x[i] == cpu_arr
                cpu_eq = comp_cpu.all()

                comp_kok_gpu = x[i] == kok_gpu_arr
                kgpu_eq = comp_kok_gpu.all()

                comp_gpu = x[i] == gpu_arr
                gpu_eq = comp_gpu.all()
                                
                if cpu_eq == True:
                    config.append("CPU")
                    # log.lammps for CPU has no extra feature
                    config.append("CPU")
                elif gpu_eq == True:
                    config.append("GPU")
                elif kgpu_eq == True:
                    config.append("Kokkos/GPU")

        if "Rhodopsin" in file_type:
            sim_type = "Rhodopsin"
            file_type = np.array(file_type)
            x = file_type.reshape(int(len(file_type)/2),2)
            no_opt_arr = ['Rhodopsin', 'Rhodopsin']
            uomp_arr = ['OMP', 'Rhodopsin']
            kok_omp_arr = ['Kokkos', 'Rhodopsin']
            for i in range(0, len(x)):
                comp_no_opt = x[i] == no_opt_arr
                no_opt_eq = comp_no_opt.all()

                comp_kok_omp = x[i] == kok_omp_arr
                komp_eq = comp_kok_omp.all()

                comp_uomp = x[i] == uomp_arr
                uomp_eq = comp_uomp.all()
                                
                if no_opt_eq == True:
                    config.append("MPI")
                    config.append("MPI")
                elif komp_eq == True:
                    config.append("Kokkos/OMP")
                elif uomp_eq == True:
                    config.append("OMP")


        mpi_break = extract_MPI_breakdown(full_line, sorter)

        extract_walltime(walltime, wall_out)

        extract_performance(perf, perf_out)

        extract_tasks_threads_nodes(nprocs_str, mpi_omp, mpi_grid, sim_type)

        log_lammps = create_data(mpi_break, wall_out, perf_out, config, mpi_tasks, omp_threads, num_nodes, num_atoms)

        return(log_lammps)
"""        
if __name__ == "__main__":
    x = extract_data(sys.argv[1:])
    print(x)
"""