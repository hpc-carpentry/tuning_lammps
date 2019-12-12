---
layout: lesson
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---
# About the Lesson
In this lesson, we will work on to focus on various accelerating modules that are implemented in LAMMPS for achieving a performance gain. First, we will discuss about the various options and then I'll show you an example to demonstrate how to decide on input parametrs to gain a performance boost. In the practical session, you will get a chance to work on another LAMMPS problem to test some of the accelearting tools that are embedded in LAMMPS. 

The content of the lesson is as follows:

1. __Why should I take this course?__
    * Why should I bother about software performance?
    * What can I expect to learn from this course?

2. __What is performance?__
    * What is the difference between software and hardware performance?
    * How can I measure performance?
        * What is Flop?
        * What is walltime?
        * What is cpuh?
    * What are the factors affecting performance?

3. __How do I benchmark software performance in HPC?__
    * What is benchmarking?
    * What are the factors that can affect a benchmark?
    * _**Case study 1:**_ A simple benchmarking example of LAMMPS in a HPC
    * _**Hands-on 1:**_ Can you do it on your own?

4. __Can I accelerate performance?__
    * Hardware acceleration and software acceleration
        * multi-core cpu
        * GPU

    * Can I use specialised code to extract best of an available hardware?
        * Multi-threading via OpenMP: parallel processing in shared memory platform
            * Thread based parallelism
            * Important run-time environment variables
            * bottlenecks in an OpenMP applications
                * hyperthreading
                * cpu affinity

        * Multi-threading via CUDA: host-device relationship
            * bottlenecks in host-device architectures

    * What if I need more workers than that available in a single node?
        * How using MPI we can acheive this?
        * What is the bottleneck here?
            - communication overhead
            - domain decomposition

    * Is this possible to use optimized library/code to get acceleration?
        *  Brief mention about various optimized libraries like MKL, FFTW

5. __What is scaling?__
    * Quntifying speedup: t<sub>1</sub>/t<sub>p</sub>
    * Am I wasting my resourse?
        * _**Case Study 2:**_ Get scaling data for a LAMMPS run
        * _**Hands-on 2:**_ Do a scaling analysis 

6. __Identifying bottlenecks in LAMMPS__
    * _**Case study 3:**_ Understand the task timing breakdown of LAMMPS output
    * _**Hands-on 3:**_ Understand the task timing breakdown of LAMMPS output of a different problem

7. __How can I accelerate LAMMPS performance?__

    * Knowing what hardwares LAMMPS can be used on

    * How can I enable arcitecture support at runtime?

        * Accelerator packages in LAMMPS
            * What packages for which architecture?
                * OPT
                * USER-OMP
                * USER-INTEL
                * GPU
                * KOKKOS

    * Why KOKKOS?
        * What is Kokkos?
        * Important features of LAMMPS Kokkos package
        * Fixes that support KOKKOS in LAMMPS
        * Package options

8. __How do I invoke KOKKOS in LAMMPS?__
    * Transition from regular LAMMPS call to accelerated call

9. __Comapre KOKKOS/OpenMP performance with regular LAMMPS/OpenMP performance__

    * _**Case study 4:**_ using OpenMP+KOKKOS for Skylake AVX-512 architecture
    * Comparing LAMMPS performance between runs with and without KOKKOS 
    * _**Exercise 4:**_ Similar study with slightly different problem

10. __Comapre KOKKOS/GPU performance with regular LAMMPS/GPU performance__
    * _**Case study 5:**_ using OpenMP+KOKKOS for NVIDIA Tesla V100 architecture
    * Comparing LAMMPS performance between runs with and without KOKKOS 
    * _**Exercise 5:**_ Similar study with slightly different problem

11. __What are the limitatations of different accelerator packages?__

12. __Knowing when LAMMPS is working efficiently__
    * Expected performance for given example
    * Rule of thumbs for various accelerator packages
    

## Prerequisites

> For these lessons, I'll assume that you have a prior experience on working in a HPC cluster, basic Linux/unix commands, shell scripts, and the primary knowledge to understand LAMMPS inputs files and running LAMMPS jobs in a cluster.

> To know about the basic LAMMPS commands, you may go through this [link](https://lammps.sandia.gov/doc/Commands_all.html).

>To get a basic introduction on HPC, you may follow [this](https://github.com/hpc-carpentry/hpc-intro) link.



