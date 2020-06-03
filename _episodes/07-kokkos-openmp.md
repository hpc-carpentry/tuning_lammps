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
## Using OpenMP threading through the Kokkos package
In this episode, we'll be learning to use Kokkos package with OpenMP execution for multicore CPUs. First we'll get familiarized with the command-line options to run a Kokkos OpenMP job in LAMMPS. This will be followed by a case study to gain some hands-on experience to use this package. For the hands-on part, we'll take the same rhodopsin system which we studied in episodes 4 and 5. We shall use the same input file and repeat similar scalability studies for the mixed MPI/OpenMP settings as we did it for the USER-OMP package. 

> ## Rules for performance
> 
> 1. **Know your hardware:** get the number of physical cores per node available to you. Take care such that (number of MPI tasks x OpenMP threads per task) <= Total number of physical cores per node.
> 2. **Check for hyperthreading:** Sometimes a CPU splits its each physical cores into multiple virtual cores known as threads. In Intel's term, this is called hyperthreads (HT). When hyperthreading is enabled, each physical core appears as two logical CPU units to the OS and thus allows these logical cores to share the physical execution space. This may result in a 'slight' performance gain. So, a node with 24 physical cores appears as 48 logical cores to the OS if HT is enabled. In this case, (number of MPI tasks x OpenMP threads per task) <= (Total number of physical cores per node x hardware threads).
> 3. **Fix CPU affinity:** fix me!
> 4. **Set OpenMP Environment variables:** OMP_NUM_THREADS, OMP_PROC_BIND, OMP_PLACES
{: .callout}


## Command-line options to submit a Kokkos OpenMP job in LAMMPS
In this episode, we'll learn to use Kokkos package with OpenMP for multicore CPUs. To run the Kokkos package, the following three command-line switches are very important:
  1. ```-k on``` : This enables Kokkos at runtime
  2. ```-sf kk``` : This appends the "/kk" suffix to Kokkos-supported LAMMPS styles
  3. ```-pk kokkos``` : This is used to modify the default package kokkos options
 To invoke the OpenMP execution mode with Kokkos, we need an additional command-line switch just following the ```-k on``` switch as shown below:
  4. ```-k on t Nt```: Using this switch you can specify the number of OpenMP threads that you want to use per node. You might also also need to set a proper value for the OMP_NUM_THREAD environment variables. You can do this as: ```export OMP_NUM_THREADS=4``` if you like to use 4 threads per node. 
  
> ## Get the full command-line
>
> Derive a command-line to submit a LAMMPS job for the rhodopsin system such that it invokes the Kokkos OpenMP threading to accelarte the job using 2 nodes having 40 cores each, 4 MPI ranks per nodes, 10 OpenMP threads per rank with *default* package options.
> > ## Soloution
> > ~~~
> > export OMP_NUM_THREADS=10
> > export OMP_PROC_BIND=spread
> > export OMP_PLACES=threads
> > mpirun -np 8 -ppn 4 --bind-to socket --map-by socket lmp -k on t 10 -sf kk -i in.rhodo
> > ~~~
> > {: .input}
> {: .solution}
{: .challenge}


## Find out optimum command-line settings for the *package* command
Well, there is some extra more things to do before we can jump to do a thorough scalability study when we use the Kokkos OpenMP which comes with a few extra *package* arguments and corresponding keywords (refer to the table in episode 6) as compared to that offered by the *USER-OMP* package. These are *neigh*, *newton*, *comm* and *binsize*.  First thing here that we need to do is to find what values of these keywords offer fastest runs. Once we get to know the optimum settings, we can use them for all the runs needed to perform the scalability studies.

> ## Command-lines to submit a Kokkos OpenMP job
>
> In the above, we showed a command-line example to submit a LAMMPS job with default package setting for the Kokkos OpenMP run. But, often the default *package* setting may not provide the fastest runs. Before jumping to production runs, we need to check for optimum settings for these values to avoid wastage of our time and valuable computing resources. In the very next section, we'll be showing how to do this with rhodopsin example. Before that, here I show you an example of command-line which shows how these *package* ralted keywords can be invoked in your LAMMPS run using the command-line switches. You can also invoke them by modifying the input files, but using them command-line is more convenient. An example is given below. Here we submit the job to two nodes each having 4 MPI processes. Each MPI rank is associated to 10 OpenMP threads in Kokkos mode. This is done with the switch ```-k on t 10``` and the OpenMP environment variable *OMP_NUM_THREADS*. Thread affinities are fixed through *OMP_PROC_BIND* and *OMP_PLACES*. Default *package* settings are overwritten here using ```-pk kokkos neigh half newton on comm no```. 
> > ~~~
> > export OMP_NUM_THREADS=10
> > export OMP_PROC_BIND=spread
> > export OMP_PLACES=threads
> > mpirun -np 8 -ppn 4 --bind-to socket --map-by socket lmp -k on t 10 -sf kk -pk kokkos neigh half newton on comm no -i in.rhodo
> > ~~~
{: .callout}


## Find out the optimum values of the keywords
Take the rhodopsin input files (in.rhodo and data.rhodo), and run LAMMPS jobs in 1 node for the following set of parameters with the *package* command as given in the table below. Fill in the blank spaces in the table with the walltimes (in seconds) required for these runs. Comment on which set of values give you the fastest runs.

|neigh|newton|comm|binsize|1MPI/40t|2MPI/40t|4MPI/10t|5MPI/8t |8MPI/5t|10MPI/4t|20MPI/2t|40MPI/1t|
|-----|------|----|-------|--------|--------|--------|--------|-------|-------|--------|--------|
|full | off  | no |default|    ?   |    ?   |   ?    |    ?   |   ?   |   ?   |    ?   |   ?    |
|full | off  |host|default|    ?   |    ?   |   ?    |    ?   |   ?   |   ?   |    ?   |   ?    |
|full | off  |dev |default|    ?   |    ?   |   ?    |    ?   |   ?   |   ?   |    ?   |   ?    |
|full | on   | no |default|    ?   |    ?   |   ?    |    ?   |   ?   |   ?   |    ?   |   ?    |
|half | on   | no |default|    ?   |    ?   |   ?    |    ?   |   ?   |   ?   |    ?   |   ?    | 

### Results obtained from a Skylake (AVX 512) system with 40 cores
For the Skylake (AVX 512) system with 40 cores, the results for this input is given below:

|neigh|newton|comm|binsize|1MPI/40t|2MPI/40t|4MPI/10t|5MPI/8t |8MPI/5t|10MPI/4t|20MPI/2t|40MPI/1t|
|-----|------|----|-------|--------|--------|--------|--------|-------|-------|--------|--------|
|full | off  | no |default|  172   |  139   |  123   |  125   |  120  |  117  |  116   |  118   |
|full | off  |host|default|  172   |  139   |  123   |  125   |  120  |  117  |  116   |  118   |
|full | off  |dev |default|  172   |  139   |  123   |  125   |  120  |  117  |  116   |  119   |
|full | on   | no |default|  176   |  145   |  125   |  128   |  120  |  119  |  116   |  118   |
|half | on   | no |default|  190   |  135   |  112   |  119   |  103  |  102  |  97    |  94    |

Comments: 
  1. The choice of *comm* not making practical difference. Why?
  Examine the output file carefully. It prints the following:
  ```
  WARNING: Fixes cannot yet send data in Kokkos communication, switching to classic communication (src/KOKKOS/comm_kokkos.cpp:493)
  ```
  This means for the fixes that we are using in this calculation not yet supports Kokkos communication and hence using different values of the *comm* keyword makes no difference.
  
  2. Switching on *newton* and using *half* neighbour list make the runs faster for most of the MPI/OpenMP settings.

  When *half* neighbour list and OpenMP is being used together in Kokkos, it uses data duplication to amke it thread-safe. When you use relatively less number of threads (8 or less) this could be fastest and for more threads it becomes memory-bound and suffers from poor scalability with increasing thread-counts. If you look at the data in the above table carefully, you will notice that using 40 OpenMP threads for *neigh=half* and *newton=on* makes the run slower. On the other hand, when you use only 1 OpenMP thread per MPI rank, it requires no data duplication or atomic operations, hence it produces the fastest run.  
  
 So, we'll be using this (i.e. *neigh half newton on comm host*) for all the runs in the scalability studies below.

## Do the scalability study
 1. Figure out all the possible MPI/OpenMP combinations that you can have per node (just as you did for the USER-OMP runs in episode 5). For example, I did this study in Intel Xeon Gold 6148 (Skylake) processor with 2x20 core 2.4 GHz having 192 GiB of RAM. This means each node has 40 physical cores. So, to satify the relation, *Number of MPI processes* x *Number of OpenMP threads* = *Number of cores per node*, I can have the following combinations per node: 1MPI/40 OpenMP threads, 2MPI/20 OpenMP threads, 4MPI/10 OpenMP threads, 5MPI/8 OpenMP threads, 8MPI/5 OpenMP threads, 10MPI/4 OpenMP threads, 20MPI/2 OpenMP threads, and 40MPI/1 OpenMP threads. I like to see scaling, say up to 10 nodes or more. This means that I have to run a total 80 calculations for 10 nodes since I have 8 MPI/OpenMP combinations for each node. Run the jobs for all possible combinations in your HPC system.
2. Calculate *parallel efficiency* for each of these jobs. To get the total time taken by each job, search for "wall time" in the log/screen output files.
4. Make a plot of *parallel efficiency* versus *number of nodes*.
5. Also, make a comparison of the parallel performance between the USER-OMP and Kokkos implementations of the OpenMP threading.
5. Write down your observation and make comments on any performance enhancement when you compare these results with the pure MPI runs.

### Solution
The plot is shown below. The main observations are outlined here:
  1. Data for the pure MPI-based run is plotted with the thick blue line. Strikingly, none of the Kokkos based MPI/OpenMP mixed runs show comparable parallel performance with the pure MPI-based approach. The difference in parallel efficiency is more pronounced for less node counts and this gap in performance reduces slowly as we increase more nodes to run the job. This looks like to see comaparable performance with the pure MPI-based runs we need to increase number of nodes far beyond than what is used in the current study. 
  2. If we now compare the performance of Kokkos OpenMP with the threading impleted with the USER-OMP package, there is quite a bit of difference.
  3. This difference could be due to vectorization. Currently (version 7Aug19 or 3Mar20) the Kokkos package in LAMMPS doesn't vectorize well as compared to the vectorization implemented in the USER-OMP package. USER-INTEL should be even better than USER-OMP at vectorizing if the styles are supported in that package.
  4. The 'deceleration' is probably due to Kokkos and OpenMP overheads to make the kernels thread-safe.
  5. If we just compare the performance among the Kokkos OpenMP runs, we see that parallel efficiency values are converging even for more thread-counts (1 to 20) as we increase the number of nodes. This is indicative that Kokkos OpenMP scales better with increasing thread counts as compared to the USER-OMP package.

![scaling_rhodo_kokkos_omp](../fig/07/scaling_rhodo_kokkos_omp.png)

{% include links.md %}
