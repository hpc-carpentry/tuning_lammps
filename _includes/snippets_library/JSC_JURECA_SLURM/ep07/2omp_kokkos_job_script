#!/bin/bash -x

# Ask for 1 nodes of resources for an MPI/OpenMP job for 5 minutes

#SBATCH --account=ecam
#SBATCH --nodes=1
#SBATCH --output=mpi-out.%j
#SBATCH --error=mpi-err.%j
#SBATCH --time=00:10:00

# Let's use the devel partition for faster queueing time since we have a tiny job.
# (For a more substantial job we should use --partition=batch)

#SBATCH --partition=devel

# Make sure that the multiplying the following 2 gives ncpus per node (24)

#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=12

# Prepare the execution environment
module purge
module use /usr/local/software/jureca/OtherStages
module load Stages/Devel-2019a
module load intel-para/2019a
module load LAMMPS/3Mar2020-Python-3.6.8-kokkos

# Also need to export the number of OpenMP threads so the application knows about it
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
# Set some pinning hints as well
export OMP_PROC_BIND=spread
export OMP_PLACES=threads

# srun handles the MPI task placement and affinities based on the choices in the job script file
srun lmp -in in.rhodo -k on t $OMP_NUM_THREADS -sf kk
