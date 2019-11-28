---
layout: lesson
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---
# About the Lesson
In this lesson, we will work on to focus on various accelerating modules that are implemented in LAMMPS for achieving a performance gain. First, we will discuss about the various options and then I'll show you an example to demonstrate how to decide on input parametrs to gain a performance boost. In the practical session, you will get a chance to work on another LAMMPS problem to test some of the accelearting tools that are embedded in LAMMPS. 

The content of the lesson is as follows:

1. What is benchmark?
    * general definition
    * real-world example of benchmarking: assessment of understanding
    * Ask users to build a mental model to link between steps of benchmarking
2. Why benchmarking is essential?
3. Benchmarking in HPC
    * Software and hardware performance
    * Factors affecting software performances
    * Useful performance metrics in HPC
        * walltime
        * cpuh
        * Flops
        * Theoretical peak performance
4. Speed-up
    * Various ways to speed-up/accelarate a code
    * parallel processing
    * Quntifying speedup: t<sub>1</sub>/t<sub>p</sub>
    * Scaling
    * Practical: Run a simple LJ run for LAMMPS and discuss its scaling (no OPT)
5. Amdahl's Law
6. Factors affecting software performances in a HPC
    * cpu frequency
    * number of cores per node
    * memory
    * inter-node communications: latency
    * compilers
    * algorithms
    * ways of parallelizing a code: OpenMP,MPI,CUDA
    * compute libraries
7. Ways to enhance performance
    * Identify performance bottlenecks
        * Discuss timings for LAMMPS
    * Tuning code for hardwares
    * Optimization
    * Implementing parallelization: OpenMP, MPI, CUDA
    * Further tuning using accelarting libraries
8. Accelaration packages for LAMMPS
    * OPT
    * USER-OMP
    * USER-INTEL
    * GPU
    * KOKKOS
9. Accelarating LAMMPS using GPU package
    * Basic usage
    * Case study 1: demonstration
    * Excercise 1: for users
9. Accelerating LAMMPS using KOKKOS
    * What is Kokkos?
    * Important features of LAMMPS Kokkos package
    * Fixes that support KOKKOS in LAMMPS
    * Package options
    * How to compile and run Kokkos in LAMMPS?
    * Case study 1: for Skylake AVX-512 architecture
        * Exercise 2: for users
    * Case study 2: for KNL architecture
    * Case study 3: for GPU Volta70 acrhitecture
        * Exercise 3: for users
10. Some rule of thumbs for accelarator packages
    * CPUs
    * GPUs
11. Summary

## Prerequisites

> For these lessons, I'll assume that you have a prior experience on working in a HPC cluster, basic Linux/unix commands, shell scripts, and the primary knowledge to understand LAMMPS inputs files and running LAMMPS jobs in a cluster.

> To know about the basic LAMMPS commands, you may go through this [link](https://lammps.sandia.gov/doc/Commands_all.html).

>To get a basic introduction on HPC, you may follow [this](https://github.com/hpc-carpentry/hpc-intro) link.



