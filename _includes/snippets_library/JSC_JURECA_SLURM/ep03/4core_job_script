#!/bin/bash -x

# Ask for 1 nodes (4 CPUs) of resources for an MPI job for 10 minutes

#SBATCH --account=ecam
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --output=mpi-out.%j
#SBATCH --error=mpi-err.%j
#SBATCH --time=00:10:00

# Let's use the devel partition for faster queueing time since we have a tiny job.
# (For a more substantial job we should use --partition=batch)

#SBATCH --partition=devel

# Prepare the execution environment
module purge
module use /usr/local/software/jureca/OtherStages
module load Stages/Devel-2019a
module load intel-para/2019a
module load LAMMPS/3Mar2020-Python-3.6.8-kokkos

# Run our application ('srun' handles process distribution)
srun lmp -in in.lj
