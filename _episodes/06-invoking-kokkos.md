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
In modern times, HPC industry has witnessed dramatic evolutions and we don’t know yet where will it end up! Starting from the diversifying architecture, we have also also seen a paradigm shift in accelerating code from a pure MPI -based approach. Naturally the question arises how well and how fast can we cope with such a rapid evolution? The answer “probably” lies in Kokkos that targets to ease these complexities by blending performance, portability and productivity. This is in principle done in Kokkos through abstractions targeting both parallel execution of code and data management. It supports complex node architectures with N-level memory hierarchies and multiple types of execution resources. It currently can use OpenMP, Pthreads and CUDA as backend programming models. (Most recent release: v2.8.00, February 2019).

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

