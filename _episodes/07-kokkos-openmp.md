---
title: "Kokkos with OpenMP"
teaching: 30
exercises: 15
questions:
- "How do I utilise Kokkos with OpenMP"
objectives:
- "Utilise OpenMP and Kokkos on specific hardware"
- "Do a scalability study on optimum command line settings"
keypoints:
- "The three command line switches, `-k on`, `-sf kk` and `-pk kokkos` are needed to run the Kokkos
  package"
- "Different values of the keywords `neigh`, `newton`, `comm` and `binsize` result in different
  runtimes"
---

## Using OpenMP threading through the **Kokkos** package

In this episode, we'll be learning to use **Kokkos** package with OpenMP execution for
multi-core CPUs. First we'll get familiarized with the command-line options to run a
**Kokkos** OpenMP job in LAMMPS. This will be followed by a case study to gain some
hands-on experience to use this package. For the hands-on part, we'll take the same
rhodopsin system which we studied in previous episodes. We shall use the same input
file ***ADD LINK*** and repeat similar scalability studies for the mixed MPI/OpenMP
settings as we did it for the **USER-OMP** package.

> ## Factors that will impact performance
>
> 1. **Know your hardware:** get the number of physical cores per node available to you.
>    Take care such that
>    ```
>    (number of MPI tasks) X (OpenMP threads per task) <= (total number of physical cores per node)
>    ```
> 2. **Check for hyperthreading:** Sometimes a CPU splits its each physical cores into
>    multiple *virtual* cores. Intel's term for this is
>    hyperthreads (HT). When hyperthreading is enabled, each physical core appears as
>    (usually) two logical CPU units to the OS and thus allows these logical cores to share the
>    physical execution space. This may result in a 'slight' performance gain. So, a
>    node with 24 physical cores appears as 48 logical cores to the OS if HT is enabled.
>    In this case,
>    ```
>    (number of MPI tasks) * (OpenMP threads per task) <= (total number of virtual cores per node)
>    ```
> 3. **CPU affinity:** CPU affinity decides whether a thread running on a particular core is
>    allowed to migrate to another core (if the operating system thinks that is a good
>    idea). You can set *CPU affinity masks* to limit the set of cores that the thread
>    can migrate to, for example you usually do not want your thread to migrate to another
>    socket since that could mean that it is far away from the data it needs to process
>    and could introduce a lot of delay in fetching and writing data.
> 4. **Set OpenMP Environment variables:** `OMP_NUM_THREADS`, `OMP_PROC_BIND`,
>    `OMP_PLACES` are the ones we will touch here.
{: .callout}


## Command-line options to submit a **Kokkos** OpenMP job in LAMMPS

In this episode, we'll learn to use **Kokkos** package with OpenMP for multi-core CPUs.
To run the **Kokkos** package, the following three command-line switches are very important:
  1. ```-k on``` : This enables Kokkos at runtime
  2. ```-sf kk``` : This appends the "/kk" suffix to Kokkos-supported LAMMPS styles
  3. ```-pk kokkos``` : This is used to modify the default package **Kokkos** options

To invoke the OpenMP execution mode with Kokkos, we need an additional command-line
switch just following the ```-k on``` switch as shown below:
  4. ```-k on t Nt```: Using this switch you can specify the number of OpenMP threads, `Nt`,
     that you want to use per node. You should also set a proper value for your OpenMP
     environment variables. You can do this with
     ```
     export OMP_NUM_THREADS=4
     ```
     {: .bash}
     if you like to use 4 threads per node (`Nt` is 4). You should also set some other
     environment variables to help with thread placement. For best performance with
     OpenMP 4.0 or later set
     ```
     export OMP_PROC_BIND=spread
     export OMP_PLACES=threads
     ```

> ## Get the full command-line
>
> Derive a command-line to submit a LAMMPS job for the rhodopsin system such that it
> invokes the Kokkos OpenMP threading to accelerate the job using 2 nodes having 40 cores
> each, 4 MPI ranks per nodes, 10 OpenMP threads per rank with *default* package options.
> 
> > ## Solution
> > 
> > ```
> > export OMP_NUM_THREADS=10
> > export OMP_PROC_BIND=spread
> > export OMP_PLACES=threads
> > mpirun -np 8 -ppn 4 --bind-to socket --map-by socket lmp -k on t $OMP_NUM_THREADS -sf kk -i in.rhodo
> > ```
> > {: .bash}
> >
> > This solution includes affinity using OpenMPI MPI runtime binding mechanisms
> > `--bind-to socket --map-by socket` which ensures that OpenMP threads cannot move
> > between sockets (but how to set this is
> > ***dependent on the MPI runtime used***). `OMP_PROC_BIND` and `OMP_PLACES` influence
> > what happens to the OpenMP threads on each socket.
> {: .solution}
{: .challenge}


## Finding out optimum command-line settings for the `package` command

There is some more work to do before we can jump into a thorough scalability study when
we use OpenMP in **Kokkos** which comes with a few extra `package` arguments and
corresponding keywords (see the [previous episode]({{page.root}}/06-invoking-kokkos) for
a list of all options) as compared to that offered by the **USER-OMP** package. These
are `neigh`, `newton`, `comm` and `binsize`.  The first thing that we need to do here is to
find what values of these keywords offer the fastest runs. Once we know the optimum
settings, we can use them for all the runs needed to perform the scalability studies.

> ## Command-lines to submit a **Kokkos** OpenMP job
>
> In the above, we showed a command-line example to submit a LAMMPS job with default
> package setting for the Kokkos OpenMP run. But, often the default `package` setting
> may not provide the fastest runs. Before jumping to production runs, we need to check
> for optimum settings for these values to avoid wastage of our time and valuable
> computing resources. In the very next section, we'll be showing how to do this with
> rhodopsin example. Before that, here I show you an example of command-line which shows
> how these `package` related keywords can be invoked in your LAMMPS runs using the
> command-line switches. Default `package` settings are overwritten here using
> ```-pk kokkos neigh half newton on comm no```.
>
> ~~~
> export OMP_NUM_THREADS=10
> export OMP_PROC_BIND=spread
> export OMP_PLACES=threads
> mpirun -np 8 -ppn 4 --bind-to socket --map-by socket lmp -k on t $OMP_NUM_THREADS -sf kk -pk kokkos neigh half newton on comm no -i in.rhodo
> ~~~
> {: .bash}
{: .callout}

> ## The optimum values of the keywords
>
> Take the rhodopsin input files (`in.rhodo` and `data.rhodo` *** SHOULD BE LINKED *** ),
> and run LAMMPS jobs for `40 MPI/1 OpenMP` thread on 1 node using the `package`command for the
> following two set of parameters.
>
> * `neigh full new town off comm no`
> * `neigh half newton on comm host`
>
> 1. What is the influence on `comm`? What is implied in the output file?
>
> 2. What difference does switching the values of `neigh` and `newton` have? Why?
>
> > ## Results obtained from a 40 core system
> > For a HPC setup which has 40 cores per node, the runtimes for all the MPI/OpenMP combinations
> > and combination of keywords is given below:
> >
> > |neigh|newton|comm|binsize|1MPI/40t|2MPI/40t|4MPI/10t|5MPI/8t |8MPI/5t|10MPI/4t|20MPI/2t|40MPI/1t|
> > |-----|------|----|-------|--------|--------|--------|--------|-------|-------|--------|--------|
> > |full | off  | no |default|  172   |  139   |  123   |  125   |  120  |  117  |  116   |  118   |
> > |full | off  |host|default|  172   |  139   |  123   |  125   |  120  |  117  |  116   |  118   |
> > |full | off  |dev |default|  172   |  139   |  123   |  125   |  120  |  117  |  116   |  119   |
> > |full | on   | no |default|  176   |  145   |  125   |  128   |  120  |  119  |  116   |  118   |
> > |half | on   | no |default|  190   |  135   |  112   |  119   |  103  |  102  |  97    |  94    |
> >
> > 1. The influence on `comm` can be seen in the output file, as it prints the following;
> >
> >    ```
> >    WARNING: Fixes cannot yet send data in Kokkos communication, switching to classic communication (src/KOKKOS/comm_kokkos.cpp:493)
> >    ```
> >    {: .output}
> >
> >    This means the fixes that we are using in this calculation are not yet supported
> >    in **Kokkos** communication and hence using different values of the `comm` keyword
> >    makes no difference.
> >
> > 2. Switching on `newton` and using `half` neighbour list make the runs faster for
> >    most of the MPI/OpenMP settings.
> >    When `half` neighbour list and OpenMP is being used together in **Kokkos**, it
> >    uses data duplication to make it thread-safe. When you use relatively few
> >    numbers of threads (8 or less) this could be fastest and for more threads it
> >    becomes memory-bound (since there are more copies of the same data filling up
> >    RAM) and suffers from poor scalability with increasing thread-counts. If you
> >    look at the data in the above table carefully, you will notice that using 40
> >    OpenMP threads for `neigh = half` and `newton = on` makes the run slower. On the
> >    other hand, when you use only 1 OpenMP thread per MPI rank, it requires no data
> >    duplication or atomic operations, hence it produces the fastest run.
> >
> > So, we'll be using `neigh half newton on comm host`) for all the runs in the scalability
> > studies below.
> {: .solution}
{: .challenge}

> ## Do the scalability study
> 1. Figure out all the possible MPI/OpenMP combinations that you can have per node. For
>    example, I did this study on an Intel
>    Skylake node with 2x20 cores. This means each node has 40 physical cores. So, to
>    satisfy
>    ```
>    (Number of MPI processes) * (Number of OpenMP threads) = (Number of cores per node)
>    ```
>    I can have the following combinations per node:
>    * 1 MPI task with 40 OpenMP threads
>    * 2MPI tasks with 20 OpenMP threads
>    * 4MPI tasks with 10 OpenMP threads
>    * 5MPI tasks with 8 OpenMP threads
>    * 8MPI tasks with 5 OpenMP threads
>    * 10MPI tasks with 4 OpenMP threads
>    * 20MPI tasks with 2 OpenMP threads
>    * 40MPI tasks with 1 OpenMP thread
>    I like to see scaling up  to say up to 10 nodes or more. This means that I have to
>    run a total 80 calculations for 10 nodes since I have 8 MPI/OpenMP combinations for
>    each node.
>
>    Run the jobs for all possible combinations in your HPC system  ***THIS IS TOO MUCH
>    PICK 2 GOOD EXAMPLES***.
> 2. Calculate *parallel efficiency* for each of these jobs ***GIVE SOME RESULTS SO THEY
>    CAN DO THIS***.
> 4. Make a plot of *parallel efficiency* versus *number of nodes*.
> 5. Also, make a comparison of the parallel performance between the **USER-OMP** and
>    **Kokkos** implementations of the OpenMP threading.
> 5. Write down your observations and make comments on any performance enhancement when
>    you compare these results with the pure MPI runs.
>
> > ## Solution
> >
> > <p align="center"><img src="../fig/07/scaling_rhodo_kokkos_omp.png" width="50%"/></p>
> >
> > The scalability plot is shown above. The main observations are outlined here:
> >   1. Data for the pure MPI-based run is plotted with the thick blue line. Strikingly,
> >      none of the Kokkos based MPI/OpenMP mixed runs show comparable parallel
> >      performance with the pure MPI-based approach. The difference in parallel
> >      efficiency is more pronounced for less node counts and this gap in performance
> >      reduces slowly as we increase the number of nodes to run the job. This
> >      indicates that to see
> >      comparable performance with the pure MPI-based runs we need to increase the
> >      number of nodes far beyond than what is used in the current study.
> >   2. If we now compare the performance of **Kokkos** OpenMP with the threading
> >      implemented with the **USER-OMP** package, there is quite a bit of difference.
> >
> >      This difference could be due to vectorization. Currently (version `7Aug19` or
> >      `3Mar20`) the **Kokkos** package in LAMMPS doesn't vectorize well as compared
> >      to the vectorization implemented in the **USER-OMP** package. **USER-INTEL**
> >      should be even better than **USER-OMP** at vectorizing *if the styles are
> >      supported in that package*.
> >   4. The 'deceleration' is probably due to Kokkos and OpenMP overheads to make the
> >      kernels thread-safe.
> >   5. If we just compare the performance among the **Kokkos** OpenMP runs, we see that
> >      parallel efficiency values are converging even for more thread-counts (1 to 20)
> >      as we increase the number of nodes. This is indicative that **Kokkos** OpenMP
> >      scales better with increasing thread counts as compared to the **USER-OMP** package.
> {: .solution}
{: .challenge}
