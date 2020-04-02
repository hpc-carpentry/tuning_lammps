---
title: "Benchmarking, Scaling (and Load Balancing?)"
teaching: 0
exercises: 0
questions:
- "What is benchmarking?"
- "What factors affect benchmarking?"
- "How do I perform a benchmarking analysis"
- "What is scaling?"
- "How do I perform a scaling analysis"
- "!!! What is load-balancing? !!! (FIXME)"
objectives:
- "Be able to perform a benchmark analysis"
- "Be able to perform a scaling analysis"
- "Determine factors in load balancing(?!) (FIXME)"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---

## What is benchmarking?

(FIXME)

## What factors can affect a benchmark?

(FIXME)

## Case study: Benchmarking

By now you already got some understanding about how benchmarking enables you to compare the peformance of your computing system with some 'standard' systems, and thus it helps you to know whether a further fine tuning of your job is required or not. 
As a first exercise, we will start with the simplest Lennard-Jones (LJ) system as provided in the 'bench' directory of the latest LAMMPS distribution. Following this, you will be given another example and you will follow the same set of excercises and compare your results with some 'known' benchmark.

> ## Run a LAMMPS job in a HPC
> Can you list bare minimum files that you need to schedule a LAMMPS job in a HPC?
> > ## Solution
> > For running a LAMMPS job, we must need an input file, empirical potential file (optional), and a data file (optional). We need these optional files only when the empirical potential model parameters and the molecular coordinates are not defined within the LAMMPS input file. In addition, for submitting a LAMMPS job to a HPC queue, we need a batch file. In general, each HPC uses a queing system to manage all the jobs. Two such popular ones are PBS and Slurm. 
> {: .solution}
{: .challenge}

The input file for the LJ-system is given below: 
```
{% include /snippets/ep02/in.lj %}
```
{: .Input}


The timing information for this run with both 1 and 4 processors is also provided with LAMMPS distribution. So, to benchmark it would be wise to run the same job with same processor settings. Let us now create a batch file to submit this job. 


> ## Batch file to submit a LAMMPS job
>
> Here is shown the header of a SLURM script to submit a LAMMPS job using 2 nodes and 48 processors. Can you modify the necessary fields in this script to submit the job using 4 processors?
>
> ~~~
> #!/bin/bash -x
> {{ site.sched_comment }} --account=myAccount
> {{ site.sched_comment }} --nodes=2
> {{ site.sched_comment }} --ntasks-per-node=24
> {{ site.sched_comment }} --output=mpi-out.%j
> {{ site.sched_comment }} --error=mpi-err.%j
> {{ site.sched_comment }} --time=00:05:00
> {{ site.sched_comment }} --partition=myQueue
>
> ... ... ...
> ... ... ...
> ~~~
> {: .input}
> 
> > ## Solution
> > ~~~
> > {{ site.sched_comment }} --nodes=1
> > {{ site.sched_comment }} --ntasks-per-node=4
> > ~~~
> > {: .input}
> {: .solution}
{: .challenge}

Okay, the rest part of the batch file should now be used to set the LAMMPS environment variables and finally we need to invoke the LAMMPS executable for the run. In all modern HPCs, package specific environment variables are loaded or unloaded using modules. Module is a piece of code that is load or unloaded into Kernal as required thus eliminating the requirement of system reboot each time you need to extend the functionalities of the Kernel. Here we show an example code on how to use the 'module' command to load LAMMPS in Jureca.

~~~
module use /usr/local/software/jureca/OtherStages
module load Stages/Devel-2019a
module load intel-para/2019a
module load LAMMPS/18Feb2020-cuda
~~~
{: .source}

> ## Module 
>
> In the above example, this is evident that ```LAMMPS/9Jan2020-cuda``` is the LAMMPS module that load the LAMMPS specific environment variables. Can you tell now why we loaded other modules like intel-para/2019a?
>
> > ## Solution
> > This is because this module was used to build LAMMPS and during runtime LAMMPS execuatble will look for all these libraries etc. 
> {: .solution}
{: .challenge}

Now we'll invoke LAMMPS executable to do the job. This can be done as following
```
srun lmp < in.lj
```
{: .input}

Or, if you are using ```mpirun``` instead of ```srun```, the submission line would be:
```
mpirun -np 1 lmp < in.lj
```
{: .input}

In this case, ```lmp``` is the name of the LAMMPS executable. But, in your HPC it could named something else.

> ## Slurm script: full view
>
> Just following the exercise above can you create a batch file to submit a LAMMPS job for the above input file (say, in.lj) to 1 core only. You will submit the job to a partition/queue named ```batch```. The job is expected to take not more than 5 minutes, and the ```batch``` partition allows you to submit jobs not crossing 72 hours time limit. The name of the LAMMPS executable is ```lmp```. 
>
> > ## Solution
> > ~~~
> > #!/bin/bash -x
> > {{ site.sched_comment }} --account=ecam
> > {{ site.sched_comment }} --nodes=1
> > {{ site.sched_comment }} --ntasks-per-node=1
> > {{ site.sched_comment }} --output=mpi-out.%j
> > {{ site.sched_comment }} --error=mpi-err.%j
> > {{ site.sched_comment }} --time=72:00:00
> > {{ site.sched_comment }} --partition=batch
> >
> > module use /usr/local/software/jureca/OtherStages
> > module load Stages/Devel-2019a
> > module load intel-para/2019a
> > module load LAMMPS/9Jan2020-cuda
> >
> > srun lmp < in.lj > out.lj
> > ~~~
> > {: .input}
> {: .solution}
{: .challenge}

## Understand the output files
Let us now look for the output files. You would notice that in this case three files have been created: ```log.lammps```, ```mpi-out.xxxxx```, and ```mpi-err.xxxxx```. Among these three, ```mpi-out.xxxxx``` is mainly to capture the screen output that have been generated during the job execution. The purpose of the ```mpi-err.xxxxx``` file is to log entries if there is any error occurring during run-time. The one that is created by LAMMPS is called ```log.lammps```. 

Once you open the ```log.lammps``` file you will notice that this file contains most of the important information starting from the LAMMPS version, number of processors used for the runs, processor lay out, thermdynamic steps, and the timing information. The header of a ```log.lammps``` file would be somewhat similar to this:
```
LAMMPS (18 Feb 2020)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:94)
  using 1 OpenMP thread(s) per MPI task
```
Note that it tells you about the LAMMPS version, and ```OMP_NUM_THREADS``` which is one of the important environment variables required to set for obtainging a performance boost. This would be discussed later in this tutorial. But for now, we'll focus mainly on the timing information provided in this file. 

When the run concludes, LAMMPS prints the final thermodynamic state and a total run time for the simulation. It also appends statistics about the CPU time and storage requirements for the simulation. An example set of statistics is shown here:

```
Loop time of 1.76553 on 1 procs for 100 steps with 32000 atoms

Performance: 24468.549 tau/day, 56.640 timesteps/s
100.0% CPU use with 1 MPI tasks x 1 OpenMP threads

MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 1.5244     | 1.5244     | 1.5244     |   0.0 | 86.34
Neigh   | 0.19543    | 0.19543    | 0.19543    |   0.0 | 11.07
Comm    | 0.016556   | 0.016556   | 0.016556   |   0.0 |  0.94
Output  | 7.2241e-05 | 7.2241e-05 | 7.2241e-05 |   0.0 |  0.00
Modify  | 0.023852   | 0.023852   | 0.023852   |   0.0 |  1.35
Other   |            | 0.005199   |            |       |  0.29

Nlocal:    32000 ave 32000 max 32000 min
Histogram: 1 0 0 0 0 0 0 0 0 0
Nghost:    19657 ave 19657 max 19657 min
Histogram: 1 0 0 0 0 0 0 0 0 0
Neighs:    1.20283e+06 ave 1.20283e+06 max 1.20283e+06 min
Histogram: 1 0 0 0 0 0 0 0 0 0

Total # of neighbors = 1202833
Ave neighs/atom = 37.5885
Neighbor list builds = 5
Dangerous builds not checked
Total wall time: 0:00:01
```
{: .log.lammps}

## Useful keyword to search for
  * The ```Loop time``` is the total wall-clock time for the simulation to run. (source: LAMMPS manual)
Use the following to extract this from ```log.lammps```:
```
grep "Loop time" log.lammps| sed 's/|/ /' | awk '{print $4}'
```
```
xxx]$ 1.76553
```

  * The Performance line is provided for convenience to help predict how long it will take to run a desired physical simulation.  (source: LAMMPS manual)
Use the following command line to extract the value in units of ```tau/day``` :
```
grep "Performance" log.lammps| sed 's/|/ /' | awk '{print $2}'
```
```
xxx]$ 24468.549
```

  * The CPU use line provides the CPU utilization per MPI task; it should be close to 100% times the number of OpenMP threads (or 1 of not using OpenMP). Lower numbers correspond to delays due to file I/O or insufficient thread utilization. (source: LAMMPS manual)
Use the following command line to extract the value in units of ```tau/day``` :
```
grep "CPU use" log.lammps| sed 's/|/ /' | awk '{print $1}'
```
```
xxx]$ 100.0%
```
* Next, we'll discuss about the timing breakdown table for CPU runtime. If try the following command line
```
grep -A 8 "breakdown" log.lammps 
```
you should see the following output:
```
MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 1.5244     | 1.5244     | 1.5244     |   0.0 | 86.34
Neigh   | 0.19543    | 0.19543    | 0.19543    |   0.0 | 11.07
Comm    | 0.016556   | 0.016556   | 0.016556   |   0.0 |  0.94
Output  | 7.2241e-05 | 7.2241e-05 | 7.2241e-05 |   0.0 |  0.00
Modify  | 0.023852   | 0.023852   | 0.023852   |   0.0 |  1.35
Other   |            | 0.005199   |            |       |  0.29
```
The above table shows the times taken by the major categories of a LAMMPS run. A brief description of these categories has been provided in [LAMMPS manual](https://lammps.sandia.gov/doc/Run_output.html):

  * Pair = non-bonded force computations
  * Bond = bonded interactions: bonds, angles, dihedrals, impropers
  * Kspace = long-range interactions: Ewald, PPPM, MSM
  * Neigh = neighbor list construction
  * Comm = inter-processor communication of atoms and their properties
  * Output = output of thermodynamic info and dump files
  * Modify = fixes and computes invoked by fixes
  * Other = all the remaining time

This is very useful in the sense that it helps you to identify the performance bottlenecks! It will discussed later in more detail.

> ## Now run a benchmark...
>
> Now submit a LAMMPS job for the above input file in a HPC that is available to you using both 1 and 4 processors. Extract the loop times for your runs and make a bar plot to see how the performance of your HPC for this particular job compares with LAMMPS standard benchmark and with the performance for another two HPCs, Kay and Jureca.
> > | HPC system | 1 proc (sec) | 4 proc (sec) |
> > |----------- | ------------ |------------- |
> > | LAMMPS     | 2.26185      | 0.635957     |
> > | Kay        | 2.24207      | 0.592148     |
> > | Jureca     | 1.76553      | 0.531145     |
> > | your HPC   |     ?        |     ?        |
>
{: .challenge}

  * Compare this data among various HPC platforms (JSC/Kay/LAMMPS-data): Benchmark plot
  
## Scaling

Good scaling vs poor scaling. How to choose no. of nodes, preventing waste of resources.

(FIXME)

> ## Plotting performacne and number of cores
> 
> Use the code template below to analyse how performance changes based on the setup (FIXME)
> 
> ```
> code
> ```
> What do you notice about this plot?
>
{: .challenge}

### How to perform a scaling analysis

(FIXME)

### Scaling data for LAMMPS run

(FIXME)

> ## Perform a scaling analysis
>
> Using the data given, run a simple LJ run for LAMMPS and perform a scaling analysis
>
> What is the speecup of the output?
>
{: .challenge}

> ## Wasting resources
> 
> There are many factors in getting the "optimal" performance, which is dependent on the system you are dealing with. Take the code below as an example (or use the code we had in the previous excrcise??).
>
> ```
> code
> ```
> {: .bash}
>
> Which of this would be the best option to speed up performance?
> 
> 1. 
> 2. 
> 3. 
> > ## Solution
> > 
> > 1. 
> > 2. 
> {: .solution}
{: .challenge}

{% include links.md %}
