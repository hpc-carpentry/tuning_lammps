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

In the previous episode, you have learnt the basic philosophies behind various parallel
computing methods. LAMMPS is a massively-parallel molecular dynamics package that is
primarily designed with MPI-based domain decomposition as its main parallelization
strategy. It supports all of the other parallelization techniques through the use of
appropriate accelerator packages on the top of the intrinsic MPI-based parallelization.

So, is the only thing that needs to be done is decide on which accelerator package to
use? Before
using any accelerator package to speedup your runs, it is always wise to identify
performance bottlenecks. You need to ask yourself a question: Why my runs are
slower? What is it that is hindering to get the expected scaling efficiency?

## Identify bottlenecks

Identifying performance bottlenecks is important as this could save you a lot of
computation time and resources. The best way to do this is to start with a reasonably
representative system having a modest system size with run for a few hundreds/thousands
of timesteps. LAMMPS provides a timing breakdown table printed at the end of log file
and also within the screen output file generated at the end of each LAMMPS run. The
timing breakdown table has already been explained in
[earlier]({{ page.root }}/02-benchmark-and-scaling/#understand-the-output-files).

In the following section, we will work on a few examples and try to understand the
bottlenecks.

The very first thing to do is run the simulation with just one 1 MPI rank and no
threads and find a way to optimally balance between `Pair`, `Neigh`, `Comm`
***add ref to where these are explained*** and the rest. To
get a feeling for this process, let us start with a Lennard-Jones (LJ) system. We'll study
two systems: the first one is with 4,000 ***only mention number of atoms once so we the
material is easier to keep up to date*** atoms only and the other one would be quite
large, almost 10 million atoms. The following input file is for a LJ-system with an fcc
lattice ***Are comments allowed in the input files? Let's just explain the input files
there***. We can vary the system size (i.e. number of atoms) by assigning appropriate
values to the variables `x`, `y`, and `z`. The length of the run can decided by the
variable `t`. We'll choose two different system sizes here: one is tiny just having 500
***is it 4k or 500?*** atoms (`x = y = z = 10`, `t = 1000`), and the other one is huge
containing about 10M
atoms (`x = y = z = 140`, `t = 1000`). We have chosen this purposefully and let us do
serial runs, otherwise run with 1 MPI rank without any OpenMP threads. Look for the
timing breakdown table and this may provide us a way to optimally balance between `Pair`,
`Neigh`, `Comm` and the rest.


~~~
{% include /snippets/ep04/in.lj %}
~~~
{: .source}

Now let us have a look at the timing breakdown table. The following is for the small
system (having 4000 atoms). The last `%total` column in the table tells about the
percentage of the total loop time is spent in this category. Note that most of the CPU
time is spent on `Pair` part (~84%), about ~13% on the `Neigh` part and the rest of the
things have taken only 3% of the total simulation time. So, in order to get a
performance gain, the common choice would be to find a way to reduce the time taken
by the `Pair` part since improvements there will have the greatest impact on the overall
time. Often OpenMP or GPU can help us to achieve this, but not always! It very much
depends on the system that you are studying ***can we give a simple answer to "why"
here***.


> ## Timing breakdown for 4000 atoms LJ-system
> ~~~
> MPI task timing breakdown:
> Section |  min time  |  avg time  |  max time  |%varavg| %total
> ---------------------------------------------------------------
> Pair    | 12.224     | 12.224     | 12.224     |   0.0 | 84.23
> Neigh   | 1.8541     | 1.8541     | 1.8541     |   0.0 | 12.78
> Comm    | 0.18617    | 0.18617    | 0.18617    |   0.0 |  1.28
> Output  | 7.4148e-05 | 7.4148e-05 | 7.4148e-05 |   0.0 |  0.00
> Modify  | 0.20477    | 0.20477    | 0.20477    |   0.0 |  1.41
> Other   |            | 0.04296    |            |       |  0.30
> ~~~
> {: .output}
{: .callout}

The following table shows the timing breakup when the number of particles is about 10M
which is quite large! Note that, though the absolute time to complete the simulation
has increased significantly, the distribution of `%total` remains the same.

> ##  Timing breakdown for 10M atoms LJ-system
>
> ~~~
> MPI task timing breakdown:
> Section |  min time  |  avg time  |  max time  |%varavg| %total
> ---------------------------------------------------------------
> Pair    | 7070.1     | 7070.1     | 7070.1     |   0.0 | 85.68
> Neigh   | 930.54     | 930.54     | 930.54     |   0.0 | 11.28
> Comm    | 37.656     | 37.656     | 37.656     |   0.0 |  0.46
> Output  | 0.1237     | 0.1237     | 0.1237     |   0.0 |  0.00
> Modify  | 168.98     | 168.98     | 168.98     |   0.0 |  2.05
> Other   |            | 43.95      |            |       |  0.53
> ~~~
> {: .output}
{: .callout}

Now run, the same systems using all the cores available in a single node and then run
with more nodes with full capacity and note how this timing breakdown varies rapidly.
While running with multiple cores, we're using only MPI only as parallelization method.
Below we have shown the table for the small system when run with 40 MPI ranks.

> ## Timing breakdown for 10M atoms LJ-system with 40 MPI ranks
>
> ~~~
> MPI task timing breakdown:
> Section |  min time  |  avg time  |  max time  |%varavg| %total
> ---------------------------------------------------------------
> Pair    | 0.24445    | 0.25868    | 0.27154    |   1.2 | 52.44
> Neigh   | 0.045376   | 0.046512   | 0.048671   |   0.3 |  9.43
> Comm    | 0.16342    | 0.17854    | 0.19398    |   1.6 | 36.20
> Output  | 0.0001415  | 0.00015538 | 0.00032134 |   0.0 |  0.03
> Modify  | 0.0053594  | 0.0055818  | 0.0058588  |   0.1 |  1.13
> Other   |            | 0.003803   |            |       |  0.77
> ~~~
> {: .output}
{: .callout}


> ## Discussion 1
>
> Can you write down the observation that you can make from the above table? What could
> be the rationale behind such a change of the `%total` distribution among various
> categories?
>
> > ## Solution
> > The first thing that we notice in this table is that when we use 40 MPI processes
> > instead of 1 process, percentage contribution of the `Pair` part to the total
> > looptime has come down to about ~52% from 84%, similarly for the `Neigh` part also
> > the percentage contribution reduced considerably. The striking feature is that the
> > `Comm` is now taking considerable part of the total looptime. It has increased from
> > ~1% to nearly 36%. But why?
> >
> > We have 4000 total atoms. When we run this with 1 core, this handles calculations
> > (i.e. calculating pair terms, building neighbour list etc.) for all 4000 atoms. Now
> > when you run this with 40 MPI processes, the particles will be distributed among
> > these 40 cores "ideally" equally if there is no load imbalance. These cores then do
> > the calculations in parallel, sharing information when necessary. This leads to the
> > speedup. But this comes at a cost of communication between these MPI processes. So,
> > communication becomes a bottleneck for such systems where you have a small number of
> > atoms to handle and many workers to do the job. This implies that you really don't
> > need to waste your resource for such a small system.
> {: .solution}
{: .discussion}

> ## Discussion 2
>
> Now consider the following breakdown table for 1 million atom system with 40
> MPI-processes. You can see that in this case, still `Pair` term is dominating the
> table. Discuss about the rationale behind this.
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
> {: .output}
>
> > ## Solution
> > In this case, the system size is enormous. Each core will have enough atoms to deal
> > with so it remains busy in computing and the time taken for the communication is
> > still much smaller as compared to the "real" calculation time. In such cases, using
> > many cores is actually beneficial. One more thing to note here is the second last
> > column `%varavg`. This is the percentage by which the max or min varies from the
> > average value. A value near to zero implies perfect load balance, while a large
> > value indicated load imbalance. So, in this case, there is a considerable amount of
> > load imbalance specially for the `Comm` and `Pair` part. To improve the performance,
> > one may like to explore a way to minimize load imbalance. Two commands could be
> > helpful for this: *processor* and *balance*.
> {: .solution}
{: .discussion}

Let us now work on another example from LAMMPS `bench` directory with the input file
below. Let's run it using
1 core (i.e., in *serial*) with `x = y = z = 1`, and `t = 10,000`.
~~~
{% include /snippets/ep04/in.chain %}
~~~
{: .source}

This gives the timing output

> ## Timing breakdown for system with low average number of neighbours
>
> ~~~
> Section |  min time  |  avg time  |  max time  |%varavg| %total
> ---------------------------------------------------------------
> Pair    | 20.665     | 20.665     | 20.665     |   0.0 | 18.24
> Bond    | 6.9126     | 6.9126     | 6.9126     |   0.0 |  6.10
> Neigh   | 57.247     | 57.247     | 57.247     |   0.0 | 50.54
> Comm    | 4.3267     | 4.3267     | 4.3267     |   0.0 |  3.82
> Output  | 0.000103   | 0.000103   | 0.000103   |   0.0 |  0.00
> Modify  | 22.278     | 22.278     | 22.278     |   0.0 | 19.67
> Other   |            | 1.838      |            |       |  1.62
> ~~~
> {: .output}
{: .callout}

> ## Discussion 3
>
> Note that, in this case,
> the time spent in solving the `Pair` part is quite low as compared to the `Neigh`
> part. What do you thank about that may have caused such an outcome?
>
> > ## Solution
> > This kind of timing breakdown generally indicates either there is something wrong
> > with the input or a very, very unusual system geometry. If you investigate the
> > screen or log file carefully, you would find that this is a system with a very
> > short cutoff (1.12 sigma) resulting in on average less than 5 neighbors per atoms
> > (`Ave neighs/atom = 4.85891`) and thus spending very little time on computing
> > non-bonded forces. Being a sparse system, the necessity of rebuilding its neighbour
> > lists is more frequent and this explains why the time spent of the `Neigh` part is
> > much more (about 50%) than the `Pair` part (~18%). On the contrary, the LJ-system
> > is the extreme opposite. It is a relatively dense system having the average number
> > of neighbours per atom nearly 37 (`Ave neighs/atom = 37.4618`). More computing
> > operations are needed to decide the pair forces per atom (~84%), and less frequent
> > would be the need to rebuild the neighbour list (~10%).  So, here your system
> > geometry is the bottleneck that causes the neighbour list building to happen too
> > frequently and taking a significant part of the entire simulation time.
> {: .solution}
{: .discussion}

## MPI vs OpenMP

By now probably you have developed some understanding on how can you use the timing
breakdown table to identify performance bottlenecks in a LAMMPS run. But identifying
the bottleneck is not enough, you need to decide what strategy would 'probably' be more
sensible to apply in order to unblock the bottlenecks. The basic perception of speeding
up a calculation is to employ some form of *parallelization*. We have already discussed in
Episode 3 ***add reference*** that there are many ways to implement parallelism in a
code. MPI based parallelism using domain decomposition lies at the core of LAMMPS. Atoms
in each domain are associated to 1 MPI task. This domain decomposition approach comes
with a cost however, keeping track and coordinating things among these domains requires
communication overhead. It could lead to significant drop in performance if you have
limited communication bandwidth, or load imbalance in your simulation, or if you wish
to scale to a very large number of cores.

While MPI offers domain based parallelization, one can also use paralleization over
particles. This can be done using OpenMP which is a different parallelization paradigm
based on threading. This multithreading is *conceptually* easy to implement. Moreover,
OpenMP parallelization is orthogonal to MPI parallelization which means you can use
them together. OpenMP also comes with an overhead: starting and stopping OpenMP takes
compute time, OpenMP needs to be careful about how it handles memory (which can be
expensive depending on the implemenation), the particular use case impacts the
efficiency. Remember that, in general, a threaded parallelization method in LAMMPS
may not be as efficient as MPI unless you have situations where domain decomposition
is no longer efficient (we will see below how to recognise such situations).

Let us discuss a few situations:
  1. The LJ-system with 4000 atoms (discussed above): Communication bandwidth with more
     MPI processes. ("when you have too few atoms per domain. at some point LAMMPS will
     scale out and not run faster or even run slower, if you use more processors via
     MPI only. with a pair style like lj/cut this will happen at a rather small number
     of atoms")
  2. The LJ-system with with 10M atoms (discussed above): More atoms per processor,
     still communication is not a big deal in this case. ("This happens because you have
     a dense, homogeneous, well behaved system with a sufficient number of atoms, so
     that the MPI parallelization can be at its most efficient.")
  3. For inhomogeneous system or slab systems where there could be lots of empty spaces
     in the simulation cell, the number of atoms handled across these domains will vary
     a lot resulting in severe load balancing issue. While some of the domains will be
     over-subscribed, some of them will remain under-subscribed causing these domains
     (cores) less efficient in terms of performance. Often this could be improved by
     using the *processor*s keyword in a smart fashion, beyond that, there are the load
     balancing commands (*balance* command) and changing the communication using
     recursive bisecting and decomposition strategy. This might not help always since
     some of the systems are pathological. In such cases, a combination of MPI and
     OpenMP could often provide better parallel efficiency as this will result in
     larger subdomains for the same number of total processors and if you parallelize
     over particles using OpenMP threads, generally it does not hamper load balancing
     in a significant way. So, a sensible mix of MPI, OpenMP and the *balance* command
     can help you to fetch better performance from the same hardware.
  4. In mant MD problem, we need to deal with the calculation of electrostatic
     interactions. Unlike the pair forces, electrostatic interactions are long range by
     nature. To compute this long range interactions, very popular methods in MD are
     *ewald* and *pppm*. These long range solvers perform their computations in
     K-space. In case of *pppm* extra overhead results from the 3d-FFT, where as the
     Ewald method suffers from the poor O(N^(3/2) scaling and this will drag down the
     overall performance when you use more cores to do your calculation even though the
     pair part exhibits linear scaling. This is also a potential case where a hybrid
     run comprising of MPI and  OpenMP might give you better performance and improve
     the scaling.

Let us now build some hands-on experience to develop some feeling on how this works.

## Situation practice: Rhodopsin system
The input file (given below) is prepared following the inputs provided in the *bench*
directory of the LAMMPS distribution (version 7Aug2019). Using this you do a simulation
of all-atom rhodopsin protein in solvated lipid bilayer with CHARMM force field,
long-range Coulombics interaction via PPPM (particle-particle particle mesh),
SHAKE constraints. The box contains counter-ions and a reduced amount of water to make
a 32000 atom system. The force cutoff for LJ force-field is 10.0 Angstroms, neighbor
skin cutoff is 1.0 sigma, number of neighbors per atom is 440. NPT time integration
is performed for 20,000 timesteps.

<p align="center"><img src="../fig/ep04/rhodo.png" width="50%"/></p>

~~~
{% include /snippets/ep04/in.rhodo %}
~~~
{: .output}

The commandline to submit this job would be similar to this, if you want to submit the
job using 4 processors ***USE SUBSTITUTIONS HERE***:
~~~
mpirun -np 4 lmp -var x 1 -var y 1 -var z 1 -var t 20000 -in in.rhodo
~~~
{: .bash}

> ## Devise a strategy
>
> 1. Using the above input and for a fixed system size (e.g. 32,000 atoms), run
>    multiple jobs with varying processor counts starting with 1 core. For example, I
>    did this study in Intel Xeon Gold 6148 (Skylake) processor with 2x20 core 2.4 GHz
>    having 192 GiB of RAM. This means each node has 40 physical cores. So, you can
>    run jobs with 1, 4, 8, 16, 32, 40 processors first and then run with 80, 120,
>    160, 200, 240, 280, 320, 360, 400 cores, and so on. (depending on the
>    availability).
> 2. For each of these jobs, you will get timing breakdown from the screen/log file.
>    Plot the *speedup factor* versus *number of cores* for the `Pair`, `Bond`,
>    `Kspace`, `Neigh`, `Comm` and `total wall time`. A python script is provided in
>    this folder (***Fix Me***) to do the plotting.
>    *Speedup factor* = *average time taken by n processor* / *average time taken by 1 processor*
> 3. Write down your observations about how different parts of the job (i.e. pair
>    calculation, long range solver, communication, etc.) scales with increasing number
>    of cores.
> 4. Discuss with you neighbour about the bottlenecks in this calculation and devise a
>    strategy to unblock the bottleneck.
>
> > ## Solution
> >
> > <p align="center"><img src="../fig/ep04/rhodo_speedup_factor_scaling.png" width="50%"/></p>
> >
> > 1. In this calculation we used Intel Skylake processor with 40 physical cores. The
> >    job was run with 1, 4, 8, 16, 32, 40, 80, 120, 160, 200, 240, 280, 320, 360 and
> >    400 cores.
> > 2. Speedup factors were calculated and plotted. Plot is shown above ***missing legend***.
> > 3. `Pair` part and `Bond` part show almost perfect linear scaling, whereas `Neigh`
> >    and `Kspace` show poor scalability, and the total walltime also suffers from the
> >    poor scalability when running with more number of cores.
> > 4. This resembles the situation 4 discussed above. A mix of MPI and OpenMP could be
> >    a sensible approach.
> {: .solution}
{: .challenge}

> ## Load balancing
>
> One important issue with MPI-based
> parallelization is that it can under-perform for systems with inhomogeneous
> distribution of particles, or systems having lots of empty space in them. It is pretty
> common that the evolution of simulated systems evolve over time to reflect such a case.
> This results in *load imbalance*. While some of the processors are assigned with
> finite number of
> particles to deal with for such systems, a few processors could have far less atoms (or
> none) to do any calculation and this results in an overall loss in parallel efficiency.
> This situation is more likely to expose itself as you scale up to a large
> large number of processors.
>
> Is there any way to deal with load imbalance in LAMMPS?
> > Yes, you can deal it up to a certain extent using ```processors``` and ```balance```
> > commands in LAMMPS. Detail usage is given in LAMMPS manual. (Fix Me: Might be
> > discussed to some extent in later episodes)
{: .callout}
