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
> 1. **Know your hardware:** get the number of physical cores per node available to you. Take care such that (number of MPI tasks x OpenMP threads per task) <= Total number of physical cores per node.
> 2. **Check for hyperthreading:** Sometimes a CPU splits its each physical cores into multiple virtual cores known as threads. In Intel's term, this is called hyperthreads (HT). When hyperthreading is enabled, each physical core appears as two logical CPU units to the OS and thus allows these logical cores to share the physical execution space. This may result in a 'slight' performance gain. So, a node with 24 physical cores appears as 48 logical cores to the OS if HT is enabled. In this case, (number of MPI tasks x OpenMP threads per task) <= (Total number of physical cores per node x hardware threads).
> 3. **Fix CPU affinity:** fix me!
> 4. **Set OpenMP Environment variables:** OMP_NUM_THREADS, OMP_PROC_BIND, OMP_PLACES
{: .callout}

> ## First working example
>
> Let us do the following to get a feel for this package:
> 1. First, run a LAMMPS job for the given LJ-system using all the cores available to a node and without any accelerator package. Make a note of the walltime (loop time) for the completion of the job.
> 2. Second, we now want to use thread-parallelization using Kokkos for the above example. You know that you can have several MPI+OpenMP settings. Make a note of the number of physical cores that is available to you per node. Now write down a list of probable MPI+OpenMP combinations, e.g. 10 MPI tasks and 4 OpenMP threads if a node has 40 physical cores, keeping in mind of the following relation: (number of MPI tasks x OpenMP threads per task) <= Total number of physical cores per node.
> 3. Prepare job submission scripts for the above choices and submit the jobs. Make notes for the walltime (loop time) of the all runs.
> 4. Prepare a table to make a comparison of walltime (loop time) for the non-Kokkos and Kokkos runs and comment on your observation.
> > ~~~
> > variable	x index 7 
> > variable	y index 7
> > variable	z index 7
> >
> > variable	xx equal 20*$x
> > variable	yy equal 20*$y
> > variable	zz equal 20*$z
> >
> > units		lj
> > atom_style	atomic
> >
> > lattice		fcc 0.8442
> > region		box block 0 ${xx} 0 ${yy} 0 ${zz}
> > create_box	1 box
> > create_atoms	1 box
> > mass		1 1.0
> >
> > velocity	all create 1.44 87287 loop geom
> >
> > pair_style      lj/cut 2.5
> > pair_coeff      1 1 1.0 1.0 2.5
> >
> > neighbor	0.3 bin
> > neigh_modify	delay 0 every 20 check no
> >
> > fix		1 all nve
> >
> > thermo 50
> > thermo_style custom step time  temp press pe ke etotal density
> > run		500
> > ~~~
> {: .input}
> > ## Solution
> > ~~~
> > module load lmp_SKX
> > export OMP_NUM_THREADS=4
> > export OMP_PROC_BIND=spread
> > export OMP_PLACES=threads
> > mpirun -np 10 -ppn 10 --bind-to socket --map-by socket lmp -k on t 4 -sf kk -pk kokkos neigh half newton on comm device binsize 2.8 -i in.lj
> > ~~~
> {: .solution}
{: .challenge}

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
