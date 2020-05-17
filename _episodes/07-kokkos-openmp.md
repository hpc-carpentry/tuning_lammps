---
title: "KOKKOS with OpenMP"
teaching: 0
exercises: 0
questions:
- "How do I utilise KOKKOS with OpenMP"
objectives:
- "Utilise OpenMP and KOKKOS in specific hardware"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---

## KOKKOS and OpenMP
In this episode, we'll learn to use Kokkos package with OpenMP for multicore CPUs. To run the Kokkos package, the following three command-line switches are very important:
  1. ```-k on``` : This enables Kokkos at runtime
  2. ```-sf kk``` : This appends the "/kk" suffix to Kokkos-supported LAMMPS styles
  3. ```-pk kokkos``` : This is used to modify the default package kokkos options
 To invoke the OpenMP execution mode with Kokkos, we need an additional command-line switch just following the ```-k on``` switch as shown below:
  4. ```-k on t Nt```: Using this switch you can specify the number of OpenMP threads that you want to use per node. You might also also need to set a proper value for the OMP_NUM_THREAD environment variables. You can do this as: ```export OMP_NUM_THREADS=4``` if you like to use 4 threads per node. 
  
> ## Get the full command-line
>
> Derive a command-line to submit a LJ simulation in LAMMPS such that it invokes the Kokkos OpenMP threading to accelarte the job using 2 nodes having 24 cores each, 4 MPI ranks per nodes, 6 OpenMP threads per rank with default package options.
> > ## Soloution
> > ~~~
> > export OMP_NUM_THREADS=6
> > srun --nodes=2 --ntasks=4 --cpus-per-task=6 lmp -k on t 6 -sf kk -in in.lj 
> > ~~~
> > {: .input}
> {: .solution}
{: .challenge}

> ## Rules for performance
> 
> **1. Know your hardware:** get the number of physical cores per node available to you. Take care such that (number of MPI tasks x OpenMP threads per task) <= Total number of physical cores per node.
> **2. Check for hyperthreading:** Sometimes a CPU splits its each physical cores into multiple virtual cores known as threads. In Intel's term, this is called hyperthreads (HT). When hyperthreading is enabled, each physical core appears as two logical CPU units to the OS and thus allows these logical cores to share the physical execution space. This may result in a 'slight' performance gain. So, a node with 24 physical cores appears as 48 logical cores to the OS if HT is enabled. In this case, (number of MPI tasks x OpenMP threads per task) <= (Total number of physical cores per node x hardware threads).
> **3a. Fix CPU affinity:** fix me!
> **3b. Set OpenMP Environment variables:** OMP_NUM_THREADS, OMP_PROC_BIND, OMP_PLACES
{: .callout}


> ## KOKKOS and OpenMP run
>
> In `A PREVIOUS LESSON`, you would have completed a LAMMPS run without using OpenMP. Take a note of the walltime of your previous run and now compare the performance, but this time, utilising OpenMP.
>
{: .challenge}

> ## KOKKOS and OpenMP 2
> 
> Apply what you have learned throughout this lesson and the previous challenge to a slightly different problem, outlined below. Compare the performance with and without OpenMP.
> 
> ```
> This is the problem you need to solve
> ```
> {: .bash}
{: .challenge}

## Case study 1: for Skylake AVX-512 architecture

> ##  Exercise 2: for users
> 
{: .challenge}


{% include links.md %}
