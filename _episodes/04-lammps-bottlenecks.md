---
title: "Bottlenecks in LAMMPS"
teaching: 0
exercises: 0
questions:
- "How can I identify the main LAMMPS bottlenecks?"
objectives:
- "Learn how to analyse timing data in LAMMPS"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---

In the previous episode, you have learnt the basic philosophies behind various parallel computing methods. LAMMPS is a massively-parallel molecular dynamics package where one can get performance benefits from these parallelization techniques using appropriate accelerator packages on the top of MPI-based parallelization. LAMMPS is primarily designed with MPI-based domain decomposition (DD) as its main parallelization strategy. This technique has a  deep integration with the code and in most cases one can expect considerable gain from this on modern computers where cache efficiency plays an important role. When you use DD, it helps you to work with smaller data sets that can be fitted in a cache. This is efficient since CPUs now can read data directly from cache instead of going to much slower main memory.  




## Analysing timing data in LAMMPS output

> ## Breakdown of a LAMMPS run
> 
> Examine the following output / Using the LAMMPS run previously used, analyse where the main bottlenecks are in the output.
> 
> How would you consider speeding this up? Discuss with your peers for a few minutes on the feasible options.
{: .challenge}

{% include links.md %}

