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

The very first thing  to do is running the simulation with just one 1 MPI rank and no threads and find a way to optimally balance between Pair, Neigh, Comm and the rest. To get a feeling for this process, let us start with a LJ-system. We'll study two systems: the first one is with 4,000 atoms only and the other one would be quite large, almost 10 million atoms. The following input file is for a LJ-system with an fcc lattice. We can vary the system size (i.e. number of atoms) by assigning appropriate values to the variables *x*, *y*, and *z*. The length of the run can decided by the variable *t*. We'll choose two different system sizes here: one is tiny just having 500 atoms (*x = y = z = 10, t = 1000*), and the other one is huge containing about 10M atoms (*x = y = z = 140, t = 1000*). We have chosen this purposefully and let us do serial runs, otherwise run with 1 MPI rank without any OpenMP threads. Look for the timing breakdown table and this may provide us a way to optimally balance between Pair, Neigh, Comm and the rest.

```
{% include /snippets/ep04/in.lj %}
```
{: .bash}

Now let us have a look at the timing breakdown table. The following is for the small system (having 4000 atoms). The last “%total” column in the table tells about the percentage of the total loop time is spent in this category. Note that most of the CPU time is spent on *Pair* part (~84%), about ~13% on the *Neigh* part and the rest of the things have taken only 3% of the total simulation time. So, in oreder to get a performance gain, the common perception would be to find a way to reduce the time taken by the *Pair* part. Often OpenMP or GPU can help us to achieve this, but not always! It very much depends on the system that you are studying. 

```
MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 12.224     | 12.224     | 12.224     |   0.0 | 84.23
Neigh   | 1.8541     | 1.8541     | 1.8541     |   0.0 | 12.78
Comm    | 0.18617    | 0.18617    | 0.18617    |   0.0 |  1.28
Output  | 7.4148e-05 | 7.4148e-05 | 7.4148e-05 |   0.0 |  0.00
Modify  | 0.20477    | 0.20477    | 0.20477    |   0.0 |  1.41
Other   |            | 0.04296    |            |       |  0.30
```

Fix Me! (here comes the table for 1M atom system and discuss the features)

```
MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 7070.1     | 7070.1     | 7070.1     |   0.0 | 85.68
Neigh   | 930.54     | 930.54     | 930.54     |   0.0 | 11.28
Comm    | 37.656     | 37.656     | 37.656     |   0.0 |  0.46
Output  | 0.1237     | 0.1237     | 0.1237     |   0.0 |  0.00
Modify  | 168.98     | 168.98     | 168.98     |   0.0 |  2.05
Other   |            | 43.95      |            |       |  0.53
```
{: .Timing breakdown for 10M atoms LJ-system}

Now run, the same systems using all the cores availabe in a single and then run with more nodes with full capacity and note how this timing breakdown varies rapidly. While running with multiple cores, we'll using only MPI only as paralleliztion method. Below we have shown the table for the small system when run with 40 MPI ranks.

```
MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 0.24445    | 0.25868    | 0.27154    |   1.2 | 52.44
Neigh   | 0.045376   | 0.046512   | 0.048671   |   0.3 |  9.43
Comm    | 0.16342    | 0.17854    | 0.19398    |   1.6 | 36.20
Output  | 0.0001415  | 0.00015538 | 0.00032134 |   0.0 |  0.03
Modify  | 0.0053594  | 0.0055818  | 0.0058588  |   0.1 |  1.13
Other   |            | 0.003803   |            |       |  0.77
```
> ## Discussion 1
>
> Can you write down the observation that you can make from the above table? What could be the rationale behind such a change of the *%total* distribution among various categories?
> > ## Solution
> > The first thing that we notice in this table is that when we use 40 MPI processes instead of 1 process, percentage contribution of the *Pair* part to the toatl looptime has come down to about ~52% from 84%, similarly for the *Neigh* part also the percentage contribution reduced considerably. The striking feature is that the *Comm* is now taking considerable part of the total looptime. It has increased from ~1% to nearly 36%. But why? We have 4000 total atoms. When we run this with 1 core, this handles calculations (i.e. calculating pair terms, building neighbour list etc.) for all 4000 atoms. Now when you run this with 40 MPI processes, job will be distributed among these 40 cores "ideally" equally if there is no load imbalance. These cores do the calculations parallely, and hence the speedup. But this comes at a cost of communication between these MPI processes. So, communication becomes a bottlencesk for such systems where you have less number of atoms to handle and many workers to do the job. This implies that you really don't need to waste your resource for such a small system.
> {: .solution}
{: .challenge}

> ## Discussion 2
>
> Now consider the following breakdown table for 1million atom system with 40 MPI-processes. You can see that in this case, still *Pair* term is dominating the table. Discuss about the rationale behind this.
> ~~~
> MPI task timing breakdown:
> Section |  min time  |  avg time  |  max time  |%varavg| %total
> ---------------------------------------------------------------
> Pair    | 989.3      | 1039.3     | 1056.7     |  55.6 | 79.56
> Neigh   | 124.72     | 127.75     | 131.11     |  10.4 |  9.78
> Comm    | 47.511     | 67.997     | 126.7      | 243.1 |  5.21
> Output  | 0.0059468  | 0.015483   | 0.02799    |   6.9 |  0.00
> Modify  | 52.619     | 59.173     | 61.577     |  25.0 |  4.53
> Other   |            | 12.03      |            |       |  0.92
> ~~~
> > ## Solution
> > In this case, the system size is enormous. Each core will have enough atoms to deal with so it remains busy in computing and the time taken for the communication is still much smaller as compared to the "real" calculation time. In such cases, using many cores is actually beneficial.
> {: .solution}
{: .challenge}







## Analysing timing data in LAMMPS output

> ## Breakdown of a LAMMPS run
> 
> Examine the following output / Using the LAMMPS run previously used, analyse where the main bottlenecks are in the output.
> 
> How would you consider speeding this up? Discuss with your peers for a few minutes on the feasible options.
{: .challenge}

{% include links.md %}

