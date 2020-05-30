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
{: .Timing breakdown for 4000 atoms LJ-system}

The following table shows the timing breakup when the number of partcles is about 10M which is quite large! Note that, though the abosulte time to complete the simulation has increased significantly, the distribution of *%total%* remains same.

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

Now run, the same systems using all the cores available in a single and then run with more nodes with full capacity and note how this timing breakdown varies rapidly. While running with multiple cores, we'll using only MPI only as paralleliztion method. Below we have shown the table for the small system when run with 40 MPI ranks.

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
> > The first thing that we notice in this table is that when we use 40 MPI processes instead of 1 process, percentage contribution of the *Pair* part to the toatl looptime has come down to about ~52% from 84%, similarly for the *Neigh* part also the percentage contribution reduced considerably. The striking feature is that the *Comm* is now taking considerable part of the total looptime. It has increased from ~1% to nearly 36%. But why? We have 4000 total atoms. When we run this with 1 core, this handles calculations (i.e. calculating pair terms, building neighbour list etc.) for all 4000 atoms. Now when you run this with 40 MPI processes, job will be distributed among these 40 cores "ideally" equally if there is no load imbalance. These cores do the calculations parallelly, and hence the speedup. But this comes at a cost of communication between these MPI processes. So, communication becomes a bottlencesk for such systems where you have less number of atoms to handle and many workers to do the job. This implies that you really don't need to waste your resource for such a small system.
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
> > In this case, the system size is enormous. Each core will have enough atoms to deal with so it remains busy in computing and the time taken for the communication is still much smaller as compared to the "real" calculation time. In such cases, using many cores is actually beneficial. One more thing to note here is the second last column '*%varavg*'. This is the percentage by which the max or min varies from the average value. A value near to zero implies perfect load balance, while a large value indicated load imbalance. So, in this case, there is a considerable amount of load imbalance specially for the *Comm* and *Pair* part. To improve the performance, one may like to explore a way to minimize load imablance. Two commands could be helpful for this: *processor* and *balance*. 
> {: .solution}
{: .challenge}

> ## Discussion 3
> 
> Let us now work on another example from LAMMPS *bench* directory. Input file and the corresponding timing breakdown table from the screen is given below. We ran it using 1 core (serial) and *x = y = z = 1, and t = 10,000*). Note that, in this case, the time spent in solving the *Pair* part is quite less as compared to the *Neigh* part. What do you thank about that may have caused such an outcome?
> ~~~
> {% include /snippets/ep04/in.chain %}
> ~~~
> {: .bash}
> > ## Timing breakdown:
> > ~~~
> > Section |  min time  |  avg time  |  max time  |%varavg| %total
> > ---------------------------------------------------------------
> > Pair    | 20.665     | 20.665     | 20.665     |   0.0 | 18.24
> > Bond    | 6.9126     | 6.9126     | 6.9126     |   0.0 |  6.10
> > Neigh   | 57.247     | 57.247     | 57.247     |   0.0 | 50.54
> > Comm    | 4.3267     | 4.3267     | 4.3267     |   0.0 |  3.82
> > Output  | 0.000103   | 0.000103   | 0.000103   |   0.0 |  0.00
> > Modify  | 22.278     | 22.278     | 22.278     |   0.0 | 19.67
> > Other   |            | 1.838      |            |       |  1.62
> > ~~~
> {: .output}
> > ## Solution
> > This kind of timing breakdown generally indicates either there is something wrong with the input or a very, very unusual system geometry. If you investigate the screen or log file carefully, you would find that this is a system with a very short cutoff (1.12 sigma) resulting in on average less than 5 neighbors per atoms (*Ave neighs/atom = 4.85891*) and thus spending very little time on computing non-bonded forces. Being a sparse system, the necessity of rebuilding its neighbour lists is more frequent and this explains why the time spent of the *Neigh* part is much more (about 50%) than the *Pair* part (~18%). On the contrary, the LJ-system is the extreme opposite. It is a relatively dense system having the average number of neighbours per atom nearly 37 (*Ave neighs/atom = 37.4618*). More computing operations are needed to decide the pair forces per atom (~84%), and less frequent would be the need to rebuild the neighbour list (~10%).  So, here your system geometry is the bottleneck that causes the neighbour list building too frequent and taking a significant part of the entire simulation time.
> {: .solution}
{: .challenge}

## MPI vs OpenMP
By now probably you have developed some understanding on how can you use the timing breakdown table to identify performance bottlenecks in a LAMMPS run. But identifying the bottleneck is not enough, you need to decide what startegy would 'probably' be more sensible to apply in order to unblock the bottlenecks. The basic perception of speeding up a calculation is to employ parallel workforce. We have already discussed in Episode 3 that there are many ways to implement parallelism in a code. MPI based parallelism using domain decomposition lies at the core of LAMMPS. Atoms in each domain is looked by 1 MPI task (=core). Due to having better cache locality with less number of  atoms per processor and the way memory access pattern is designed in LAMMPS, it is usually faster to use MPI-based parallelization only. Every good thing comes at a cost of something. Similar is the case for domain decomposition. DD offers enhanced cache efficiency but due to keeping track among these domains it suffers from communication overhead. It could lead to significant drop in performance if you have limited communication bandwidth, or load imbalance, or if you like to scale to a very large number of cores. 

While MPI offers domain based parallelization, one can also use paralleization over particles. This can be done using OpenMP which is a different parallelization paradigm based on threading. This multithreading is easy to implement. Moreover, OpenMP parallelization is orthogonal to MPI parallelization which means you can use them together. One importnat issue with multithreading is that you need to be very careful about probable race conditions and false sharings. It can be done either by making extra copies of data for each thread or by enforcing atomic operations. These add to overhead and lead to performance loss. Remember that a threaded parallelization method may not be as efficient as MPI unless you have situations where DD is not as efficient anymore.

Let us discuss a few situations:
  1. The LJ-system with 4000 atoms (discussed above): Communication bandwidth with more MPI processes. ("when you have too few atoms per domain. at some point LAMMPS will scale out and not run faster or even run slower, if you use more processors via MPI only. with a pair style like lj/cut this will happen at a rather small number of atoms")
  2. The LJ-system with with 10M atoms (discussed above): More atoms per processor, still communication is not a big deal in this case. 
("This happens because you have a dense, homogeneous, well behaved system with a sufficient number of atoms, so that the MPI parallelization can be at its most efficient.")
  3. For inhomogeneous system or slab systems where there could be lots of empty spaces in the simulation cell, the number of atoms handled across these domains will vary a lot resulting in severe load balancing issue. While some of the domains will be over-subscribed, some of them will remain under-subscribed causing these domains (cores) less efficient in terms of performance. Often this could be improved by using the *processor*s keyword in a smart fashion, beyond that, there are the load balancing commands (*balance* command) and changing the communication using recusive bisecting and decomposition strategy. This might not help always since some of the systems are pathological. In such cases, a combination of MPI and OpenMP could often provide better parallel efficiency as this will result in larger subdomains for the same number of total processors and if you paralleize over particles using OpenMP threads, generally it does not hamper load balancing in a significant way. So, a sensible mix of MPI, OpenMP and the *balance* command can help you to fetch better performance from the same hardware.
  4. In mant MD problem, we need to deal with the calculation of electrostatic interactions. Unlike the pair forces, electrostatic interactions are long range by nature. To compute this long range interactions, very popular methods in MD are *ewald* and *pppm*. These long range solvers perform their computations in K-space. In case of *pppm* extra overhead results from the 3d-FFT, where as the Ewald method suffers from the poor O(N^(3/2) scaling and this will drag down the overall performance when you use more cores to do your calculation even though the pair part exhibits linear scaling. This is also a potenytial case where a hybrid run comprising of MPI and  OpenMP might give you better performance and improve the scaling. 
  
Let us now build some hands-on experience to develop some feeling on how this works.

## Situation practice: Rhodopsin system
The input file (given below) is prepared following the inputs provided in the *bench* directory of the LAMMPS distribution (version 7Aug2019). Using this you do a simulation of all-atom rhodopsin protein in solvated lipid bilayer with CHARMM force field, long-range Coulombics interaction via PPPM (particle-particle particle mesh), SHAKE constraints. The box contains counter-ions and a reduced amount of water to make a 32000 atom system. The force cutoff for LJ force-field is 10.0 Angstroms, neighbor skin cutoff is 1.0 sigma, number of neighbors per atom is 440. NPT time integration is performed for 20,000 timesteps.

![Rhodopsin_in_lipid_bilayer](../fig/ep04/rhodo.png)

```
{% include /snippets/ep04/in.rhodo %}
```
{: .bash}

The commandline to submit this job would be similar to this, if you want to submit the job using 4 processors:
```
mpirun -np 4 lmp -var x 1 -var y 1 -var z 1 -var t 20000 -in in.rhodo
```

> ## Decide a strategy
>
> 1. Using the above input and for a fixed system size (e.g. 32,000 atoms), run multiple jobs with varying processor counts starting with 1 core. For example, I did this study in Intel Xeon Gold 6148 (Skylake) processor with 2x20 core 2.4 GHz having 192 GiB of RAM. This means each node has 40 physical cores. So, you can run jobs with 1, 4, 8, 16, 32, 40 processors first and then run with 80, 120, 160, 200, 240, 280, 320, 360, 400 cores, and so on. (depending on the availability). 
> 2. For each of these jobs, you will get timing breakdown from the screen/log file. Plot the *speedup factor* versus *number of cores* for the *Pair*, *Bond*, *Kspace*, *Neigh*, *Comm* and *total wall time*. A python script is provided in this folder (Fix Me) to do the plotting. *Speedup factor* = *average time taken by n processor* / *average time taken by 1 processor*
> 3. Write down your observations about how different parts of the job (i.e. pair calculation, long range solver, communication, etc.) scales with increasing number of cores.
> 4. Discuss with you neighbour about the bottlenecks in this calculation and device a strategy to unblock the bottleneck.
> > ## Solution
> > 1. In this calculation we used Intel Skylake processor with 40 physical cores. The job was run with 1, 4, 8, 16, 32, 40, 80, 120, 160, 200, 240, 280, 320, 360 and 400 cores.
> > 2. Speedup factors were calculated and plotted. Plot is shown below.
> > 3. *Pair* part and *Bond* part show almost perfect linear scaling, whereas *Neigh* and *Kspace* show poor scalability, and the total walltime also suffers from the poor scalability when running with more number of cores. 
> > 4. This resembles with the situation 4 discussed above. A mix of MPI and OpenMP could be sensible approach.
> {: .solution}
{: .challenge}

![rhodo_speedup_factor_scaling](../fig/ep04/rhodo_speedup_factor_scaling.png)


