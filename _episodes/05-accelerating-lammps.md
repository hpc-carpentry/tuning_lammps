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
Well, there are two basic approaches to speed-up LAMMPS. One is to use better algorithm for certain types of calculation, and the other one is to use highly optimized codes via various "accelerator packages" deviced for hardware specific platforms. 

One popular example of first type of approach is to use the Wolf summation method instead of the Ewald summation method for calcultaing long range Coulomb interaction effectively using a short-range potential. Similarly there are a few FFT schemes are offered by LAMMPS and a user has to make a trade-off between accuracy and performance depending on his computational needs. The current tutorial is not aimed to discuss such types of algorithm based speed-up of LAMMPS rather we'll be discussing mainly on a few accelerator packages that is used to extract the most out of an available hardware of a HPC system.

There are five accelerator packages currently offered by LAMMPS. These are **OPT**, **USER-INTEL**, **USER-OMP**, **GPU** and **Kokkos**. Specialized codes contained in these packages help LAMMPS to perform well on modern HPC platforms which could have different hardware partitions. Therefore, the very next question that arises that what are these hardwares that are supported by these packages?

> ## Supported hardwares
>
> | Hardware | Accelarators |
> | -------- | ------------ |
> | Multi-core CPUs | OPT, USER-INTEL, USER-OMP, Kokkos |
> | Intel Xeon Phi | USER-INTEL, Kokkos |
> | NVIDIA GPU | GPU, Kokkos |
>
{: .callout}

Within the limited scope of this tutorial, this is almost impossible to discuss all of the above packages here. The key point to understand here is that the acceleration is achieved by multithreading either through OpenMP or GPU. The ONLY accelerator package that supports both kinds of hardwares is **Kokkos**. Kokkos is a templated C++ library developed in Sandia National Laboratory and this helps to create an abstraction that allows a *single implementation* of a software application on different kinds of hardwraes by simply mapping C++ kernel onto various backend languages. 

Before discussing on Kokkos, we'll touch a few key points about other accelerator packages to give you a feel about what these packages offer and in many cases these pakckages outperform Kokkos in its current form! 

> ## Kokkos: a developing library
>
> Most of the accelerator packages offered by LAMMPS may outperform Kokkos. Can you think of then why should we bother to learn using Kokkos?
{: .challenge}

> ## OPT package
>
> In this case, the acceleration is mainly acheived by using templeted C++ library to reduce computational overheads due to if tests and other conditional code blocks.
> This also provides better vectorization operations as compared to its regular CPU version.
> Only a handful of pair styles can be accelerated using this package. As of *3Mar20* version of LAMMPS, 10 pair styles are supported by this accelerator package. These are *pair_eam_alloy*, *pair_eam_fs*, *pair_eam*, *pair_lj_charmm_coul_long*, *pair_lj_cut_coul_long*, *pair_lj_cut*, *pair_lj_cut_tip4p_long*, *pair_lj_long_coul_long*, *pair_morse* and *pair_ufm*.
> This generally offers 5-20% savings on computational cost on most of the machines
> > ## Effect on timing breakdown table
> > 
> > We have discussed earlier that at the end of each run LAMMPS prints a timing breakdown table where it categorises the spent time into several categories like *Pair*, *Bond*, *Kspace*, *Neigh*, *Comm*, *Output*, *Modify*, *Other*. Can you make a justified guess about which of these category could be affected by the use of the *OPT* package?
> > > ## Solution
> > > The *Pair* component will see a reduction in cost since this accelerator package aims to work on the pair styles only.
> > {: .solution}
> {: .challenge}
{: .callout}



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
