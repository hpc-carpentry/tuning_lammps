#!/bin/bash -x
#SBATCH --account=ecam
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --output=mpi-out.%j
#SBATCH --error=mpi-err.%j
#SBATCH --time=00:15:00
#SBATCH --partition=devel

module use /usr/local/software/jureca/OtherStages
module load Stages/Devel-2019a
module load intel-para/2019a
module load LAMMPS/9Jan2020-cuda

srun lmp < in.lj|tee out.lj
