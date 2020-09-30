#!/bin/bash -x

# Ask for 1 nodes of resources for an MPI/GPU job for 10 minutes

#SBATCH --account=ecam
#SBATCH --nodes=1
#SBATCH --output=mpi-out.%j
#SBATCH --error=mpi-err.%j
#SBATCH --time=00:10:00

# Configure the GPU usage (we request to use all 4 GPUs on a node)
#SBATCH --partition=develgpus
#SBATCH --gres=gpu:4

# Use this many MPI tasks per node (maximum 24)
#SBATCH --ntasks-per-node=24

module purge
module use /usr/local/software/jureca/OtherStages
module load Stages/Devel-2019a
module load intel-para/2019a
# Note we are loading a different LAMMPS package
module load LAMMPS/9Jan2020-cuda

srun lmp -in in.lj -sf gpu -pk gpu 4 neigh no newton off split -1.0
