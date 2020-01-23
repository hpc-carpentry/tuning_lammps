---
layout: page
title: Introduction to HPC Lesson Outline
---

## How to use this outline

The following list of items is meant as a guide on what content should go where in this repo. This should work as a guide where you can contribute. If a bullet point is prefixed by a file name, this is the lesson where the listed content should go into. This document is meant as a concept map converted into a flow learning goals and questions.

## Accelerating LAMMPS on a HPC 

* [index.md: Prelude](index.md):Why should I take this course?
    * Why should I bother about software performance?
    * What can I expect to learn from this course?

* [01-why-bother-performance.md: What is performance?](_episodes/01-why-bother-performance.md):brief notes on software performance
    * Why is software performance important?
    * How can I measure performance?
        * What is Flop?
        * What is walltime?
        * What is cpuh?
    * What are the factors affecting performance?

* [02-benchmark-and-scaling.md: How do I benchmark software performance in HPC?](_episodes/02-benchmark-and-scaling.md):about benchamark and scaling
    * What is benchmarking?
    * What are the factors that can affect a benchmark?
        * _**Case study 1:**_ A simple benchmarking example of LAMMPS in a HPC
        * _**Hands-on 1:**_ Can you do it on your own?    
    * What is scaling?
    * How do I perform scaling analysis?
    * Quntifying speedup: t<sub>1</sub>/t<sub>p</sub>
    * Am I wasting my resourse?
        * _**Case Study 2:**_ Get scaling data for a LAMMPS run
        * _**Hands-on 2:**_ Do a scaling analysis

* [03-acceleration.md: Can I accelerate performance?](_episodes/03-acceleration.md):brief discussion over various aspects of speeding up software performances
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
        * How using MPI we can achieve this?
        * What is the bottleneck here?
            - communication overhead
            - domain decomposition

    * Is this possible to use optimized library/code to get acceleration?
        *  Brief mention about various optimized libraries like MKL, FFTW


* [04-lammps-bottlenecks.md: Identifying bottlenecks in LAMMPS](_episodes/04-lammps-bottlenecks.md):learn to analyze timing data in LAMMPS
    * _**Case study 3:**_ Understand the task timing breakdown of LAMMPS output
    * _**Hands-on 3:**_ Understand the task timing breakdown of LAMMPS output of a different problem

* [05-accelerating-lammps.md: How can I accelerate LAMMPS performance?](_episodes/05-accelerating-lammps.md):various options to accelerate LAMMPS

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

* [06-invoking-kokkos.md: How do I invoke KOKKOS in LAMMPS?](_episodes/06-invoking-kokkos.md):technical aspects to use KOKKOS with LAMMPS
    * Transition from regular LAMMPS call to accelerated call

* [07-kokkos-openmp.md: Compare KOKKOS/OpenMP performance with regular LAMMPS/OpenMP performance](_episodes/07-kokkos-openmp.md):learn to use openmp with KOKKOS

    * _**Case study 4:**_ using OpenMP+KOKKOS for Skylake AVX-512 architecture
    * Comparing LAMMPS performance between runs with and without KOKKOS
    * _**Exercise 4:**_ Similar study with slightly different problem

* [08-kokkos-gpu.md: Compare KOKKOS/GPU performance with regular LAMMPS/GPU performance](_episodes/08-kokkos-gpu.md):learn to use gpu with KOKKOS
    * _**Case study 5:**_ using OpenMP+KOKKOS for NVIDIA Tesla V100 architecture
    * Comparing LAMMPS performance between runs with and without KOKKOS
    * _**Exercise 5:**_ Similar study with slightly different problem

* [09-limitations.md: What are the limitatations of different accelerator packages?](_episodes/09-limitations.md):discuss the limitations of KOKKOS and other accelerator packages

* [10-thumbrules.md: Knowing when LAMMPS is working efficiently](_episodes/10-thumbrules.md):thumbrules to follow
    * Expected performance for given example
    * Rule of thumbs for various accelerator packages


