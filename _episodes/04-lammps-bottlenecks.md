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

In the previous episode, you have learnt the basic philosophies behind various parallel computing methods. LAMMPS is a massively-parallel molecular dynamics package where one can get performance benefits from these parallelization techniques using appropriate accelerator packages on the top of MPI-based parallelization. LAMMPS is primarily designed with MPI-based domain decomposition (DD) as its main parallelization strategy. This technique has a  deep integration with the code and in most cases one can expect considerable gain from this on modern computers where cache efficiency plays an important role. When you use DD, it helps you to work with smaller data sets that can be fitted in a cache. This is efficient since CPUs now can read data directly from cache instead of going to much slower main memory. One important issue with MPI-based paralleilization is that it can under-perform for systems with inhomogeneous distribution of particles, or systems having lots of empty space in them. This results in load imbalance. While some of the processors are assigned with finite number of particles to deal with for such systems, a few processors could have very less atoms or none to do any calculation and this results in an overall loss in parallel efficiency. Not only this, it could also be an issue if you have limited bandwidth for nodes communications. This situation could be more relevant if you like to scale for a very large number of processors where communication could be a bottleneck. So, before using any accelerator package to speedup your runs, it is always wise to identify performance bottlenecks. You need to ask yourself a question: Why my runs are slower? What is it that is hindering to get the expected scaling efficiency? 

> ## Load balancing
>
> Is there any way to deal with load imbalance in LAMMPS?
> > Yes, you can deal it upto a certain extent using ```processors``` and ```balance``` commands in LAMMPS. Detail usage cis given in LAMMPS manual. (Fix Me: Might be discussed to some extent in later episodes)
{: .callout}

## Identify bottlenecks
Identifying performance bottleneck is important as this could save you a lot of computation time and resources. The best way to do this is to start with a representative system having a modest system size with run for a few hundreds/thousands of timesteps and then look for the timing breakdown table printed at the end of log file and the screen output file generated at the end of each LAMMPS run. The timing breakdown table has already been explained in Episode 2. In the following section, we will work on a few examples and try to understand the bottlenecks.

The very first thing  to do is running the simulation with just one 1 MPI rank and no threads and find a way to optimally balance between Pair, Neigh, Comm and the rest. To get a feeling for this process, let us start with a LJ-system. We'll study two systems: the first one is with 4,000 atoms only and the other one would be quite large, almost 10 million atoms. The input file for the small LJ system (i.e. with 4,000 atoms) is given below, and we can run either serially or with 1 MPI rank (no OpenMP threading).

```
{% include /snippets/ep02/in.lj %}
```
{: .bash}

Now let us have a look at the timing breakdown table:

```
MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 0.15331    | 0.15331    | 0.15331    |   0.0 | 81.48
Neigh   | 0.025885   | 0.025885   | 0.025885   |   0.0 | 13.76
Comm    | 0.0055292  | 0.0055292  | 0.0055292  |   0.0 |  2.94
Output  | 5.5075e-05 | 5.5075e-05 | 5.5075e-05 |   0.0 |  0.03
Modify  | 0.0025997  | 0.0025997  | 0.0025997  |   0.0 |  1.38
Other   |            | 0.0007715  |            |       |  0.41
```


## Analysing timing data in LAMMPS output

> ## Breakdown of a LAMMPS run
> 
> Examine the following output / Using the LAMMPS run previously used, analyse where the main bottlenecks are in the output.
> 
> How would you consider speeding this up? Discuss with your peers for a few minutes on the feasible options.
{: .challenge}

{% include links.md %}

