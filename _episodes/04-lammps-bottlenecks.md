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
> > Yes, you can deal it up to a certain extent using ```processors``` and ```balance``` commands in LAMMPS. Detail usage cis given in LAMMPS manual. (Fix Me: Might be discussed to some extent in later episodes)
{: .callout}

## Identify bottlenecks
Identifying performance bottleneck is important as this could save you a lot of computation time and resources. The best way to do this is to start with a representative system having a modest system size with run for a few hundreds/thousands of timesteps and then look for the timing breakdown table printed at the end of log file and the screen output file generated at the end of each LAMMPS run. The timing breakdown table has already been explained in Episode 2. In the following section, we will work on a few examples and try to understand the bottlenecks.

The very first thing  to do is running the simulation with just one 1 MPI rank and no threads and find a way to optimally balance between Pair, Neigh, Comm and the rest. To get a feeling for this process, let us start with a LJ-system. We'll study two systems: the first one is with 4,000 atoms only and the other one would be quite large, almost 10 million atoms. The following input file is for a LJ-system with an fcc lattice. We can vary the system size (i.e. number of atoms) by assigning appropriate values to the variables *x*, *y*, and *z*. The length of the run can decided by the variable *t*. We'll choose two different system sizes here: one is tiny just having 500 atoms (*x = y = z = 5, t = 1000*), and the other one is huge containing about 10M atoms (*x = y = z = 140, t = 1000*). We have chosen this purposefully and let us do serial runs, otherwise run with 1 MPI rank without any OpenMP threads. Look for the timing breakdown table and this may provide us a way to optimally balance between Pair, Neigh, Comm and the rest.

```
{% include /snippets/ep04/in.lj %}
```
{: .bash}

Now let us have a look at the timing breakdown table. The following is for the small system (having 500 atoms). The last “%total” column in the table tells about the percentage of the total loop time is spent in this category. Note that most of the CPU time is spent on *Pair* part (~81%), about ~14% on the *Neigh* part and the rest of the things have taken only 5% of the total simulation time. So, in oreder to get a performance gain, the common perception would be to find a way to reduce the time taken by the *Pair* part. Often OpenMP or GPU can help us to achieve this, but not always! It very much depends on the system that you are studying. 

```
MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 0.30249    | 0.30249    | 0.30249    |   0.0 | 81.37
Neigh   | 0.051532   | 0.051532   | 0.051532   |   0.0 | 13.86
Comm    | 0.010921   | 0.010921   | 0.010921   |   0.0 |  2.94
Output  | 1.502e-05  | 1.502e-05  | 1.502e-05  |   0.0 |  0.00
Modify  | 0.0052896  | 0.0052896  | 0.0052896  |   0.0 |  1.42
Other   |            | 0.001517   |            |       |  0.41
```

Fix Me! (here come the table for 1M atom system and discuss the features)
```
Table for 1M atoms system
```

Now run, the same systems using all the cores availabe in a single and then run with more nodes with full capacity and note how this timing breakdown varies rapidly. While running with multiple cores, we'll using only MPI only as paralleliztion method. Below we have shown the table for the small system when run with 40 MPI ranks.

```
MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 0.0027054  | 0.0030858  | 0.0037464  |   0.5 | 12.87
Neigh   | 0.00074922 | 0.00081711 | 0.00094189 |   0.0 |  3.41
Comm    | 0.018201   | 0.01898    | 0.019457   |   0.2 | 79.19
Output  | 0.0006093  | 0.00063653 | 0.0012279  |   0.0 |  2.66
Modify  | 0.00012911 | 0.00014804 | 0.00016792 |   0.0 |  0.62
Other   |            | 0.0003017  |            |       |  1.26
```
> ## Discussion 1
>
> 




## Analysing timing data in LAMMPS output

> ## Breakdown of a LAMMPS run
> 
> Examine the following output / Using the LAMMPS run previously used, analyse where the main bottlenecks are in the output.
> 
> How would you consider speeding this up? Discuss with your peers for a few minutes on the feasible options.
{: .challenge}

{% include links.md %}

