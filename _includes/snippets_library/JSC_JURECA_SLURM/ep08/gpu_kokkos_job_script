#!/bin/bash -x

# Ask for 1 nodes of resources for an MPI/GPU job for 5 minutes

#SBATCH --account=ecam
#SBATCH --nodes=1
#SBATCH --output=mpi-out.%j
#SBATCH --error=mpi-err.%j
#SBATCH --time=00:10:00

# Configure the GPU usage (we request to use all 4 GPUs on a node)
#SBATCH --partition=develgpus
#SBATCH --gres=gpu:4

# Use this many MPI tasks per node (maximum 24)
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=6

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PROC_BIND=spread
export OMP_PLACES=threads

module purge
module use /usr/local/software/jureca/OtherStages
module load Stages/Devel-2019a
module load intel-para/2019a
# Note we are loading a different LAMMPS package
module load LAMMPS/3Mar2020-gpukokkos

srun lmp -in in.lj -k on g 4 -sf kk -pk kokkos cuda/aware off
