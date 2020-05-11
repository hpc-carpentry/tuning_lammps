---
title: "Invoking KOKKOS"
teaching: 0
exercises: 0
questions:
- "How do I invoke KOKKOS with LAMMPS?"
objectives:
- "Learn how to transition from a normal LAMMPS call to an accelerated call"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---
## Kokkos
In recent times, the HPC industry has witnessed a dramatic architectural revolution. Modern HPC architecture not only includes the conventional multi-core cpus, but also manycore systems like Xeon Phis or Nvidia GPUs, and we don't know yet where this revolution will end up! With the availability of so many cores for computing, one would naturally expect a 'scalable' speedup in performance. However, this scalability does not come free-of-cost, this may require several man-years to modify an existing code to make it compatible for new hardware architectures. Why do we need to modify a code for new architectures? This is because these different hardwres were designed keeping in mind different philosophies of parallelization and these philosophies keep updating at more finer levels to enhance the performance. Some of the architectures prefer data-paralleliztion, while some of them work better for task-level parallelization. So to access the finer levels of parallisation offered by modern day architectures, we often need to use parallizing approaches other than the old classic MPI-based approach. For example, on a shared memory platform one can use OpenMP, or, on a mixed CPU+GPU platform, one can use CUDA or OpenACC to parallize their codes. The major issue with all these approaches is the performance portability which arises due to complex and varying memory access pattern across devices. So, the question arises: Is there any way to ease this difficulty?  

Kokkos is probably an answer to this portability issue. The primary objective of Kokkos is to maximize the amount of user code that can be compiled for various devices but obtaing comparable performance if the code was written in a  native language specific to that particular device. How does Kokkos achieve this goal? 

1. It maps a C++ kernel to different backend languages like Cuda, OpenMP, Pthreads.
2. It also provides data abstractions to adjust (at compile time) the memory layout of data structures like 2d and 3d arrays to optimize performance on different hardware. 


## Methodologies and checklists

## Accelerating LAMMPS using KOKKOS

## Knowing your hardware
   
## What is KOKKOS?

* supports OpenMP and GPU
* provide excellent scalability to many OpenMP threads
* 1-to-1 GPU to CPU support
* Minimal data transfer between the host and the device
* everything runs on GPU
* supports modern GPUs only
* supports double precision only

## Important features of LAMMPS Kokkos package

Kokkos can be used in conjunction with LAMMPS to accelerate its performance. This package helps to optimize LAMMPS performances for specific hardware architectures.
But to obtain the Kokkos accelartion, LAMMPS needs to be built using Kokkos for those specific hardwares and it also requires propoer choices of input parametres to get an optimal performance.

The list of LAMMPS features that is supported by Kokkos is given below:

| Atom Styles | Pair Styles  | Fix Styles  | Compute Style | Bond Styles | Angle Styles | Dihedral Styles | Improper Styles | K-space Styles |
|:----------- |:------------ |:----------- |:------------- |:----------- |:------------ |:--------------- |:--------------- |:-------------- |
| Angle       |Buck/coul/cut | Deform      | Temp          | Fene        | Charm        | Charm           | Harmonic        | Pppm           |
| Atomic      |Buck/coul/long| Langevin    |               | Harmonic    | Harmonic     | Opls            |                 |                |
| Bond        |Etc           | Momentum    |               |             |              |                 |                 |                |
| Charge      |Etc           | Nph         |               |             |              |                 |                 |                |
| Full        |              | Npt         |               |             |              |                 |                 |                |
| Molecular   |              | Nve         |               |             |              |                 |                 |                |
|             |              | Nvt         |               |             |              |                 |                 |                |
|             |              | Qeq/Relax   |               |             |              |                 |                 |                |
|             |              | Reaxc/bonds |               |             |              |                 |                 |                |
|             |              |Reaxc/species|               |             |              |                 |                 |                |
|             |              | Setforce    |               |             |              |                 |                 |                |
|             |              | Wall/reflect|               |             |              |                 |                 |                |

> ## LAMMPS hardware compatibility
> Which of these hardwares is LAMMPS compatible on?
> 
> 1. 
> 2. 
> 3. 
> ...
> > ## Solution
> > 
> > 1. 
> > 2. 
> > 3. 
> >
> {: .solution}
{: .challenge}


> ## Software vs. Hardware compatibility
> 
> Which hardwares can the following software packages be used on? There can be multiple results for each software.
> 
> > ## Solution
> > 
> > solution
> > 
> {: .solution}
{: .challenge}

## Package options: some rules of thumb

## How to compile and run Kokkos in LAMMPS?

## Case study 1: for Skylake AVX-512 architecture

> ##  Exercise 2: for users
> 
{: .challenge}

## Case study 2: for KNL architecture

## Case study 3: for GPU Volta70 acrhitecture

> ## Exercise 3: for users
> 
{: .challenge}


> ## Modifying input and submission script
> 
> Analyse the input file `input.lj` and the submission script `run.sh`
> 
> What additional modifications need to be made to make them run under (FIXME) conditions
>
{: .challenge}

{% include links.md %}

