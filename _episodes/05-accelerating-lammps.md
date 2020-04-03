---
title: "Accelerating LAMMPS"
teaching: 0
exercises: 0
questions:
- "What are the various options to accelerate LAMMPS"
- "What hardwares can LAMMPS be used on?"
- "How can I enable architecture support at runtime?"
- "What accelerator packages are compatible with which hardware?"
- "What is KOKKOS and why should I use it?"
objectives:
- "First learning objective. (FIXME)"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---
## How can I accelerate LAMMPS performance?
Well, there are two basic approaches to accelerate LAMMPS performance. One is to use better algorithm, and the other one is to device 
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

* Atom styles:
    * angle
    * atomic
    * bond
    * charge
    * full
    * molecular
* Pair styles:
    * buck/coul/cut
    * buck/coul/long
    * etc.
    * etc.
* Fix styles:
    * deform
    * langevin
    * momentum
    * nph
    * npt
    * nve
    * nvt
    * qeq/relax
    * reaxc/bonds
    * reaxc/species
    * setforce
    * wall/reflect
* Compute style:
    * temp
* Bond styles:
    * fene
    * harmonic
* Angle styles:
    * charmm
    * harmonic
* Dihedral styles:
    * charmm
    * opls
* Improper style:
    * harmonic
* K-space style:
    * pppm

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

{% include links.md %}
