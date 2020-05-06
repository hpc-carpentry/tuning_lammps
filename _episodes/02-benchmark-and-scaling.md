---
title: "Benchmarking, Scaling (FIXME and Load Balancing?)"
teaching: 0
exercises: 0
questions:
- "What is benchmarking?"
- "How do I perform a benchmarking analysis in LAMMPS"
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

To get a better example of benchmarking, let's take the example of a sprint athelete. The athelete runs a predetermined distance on a particular surface, and a time is recorded. Based on different conditions, such as how dry or wet the surface is, or what the surface is made of, grass, sand, or track, the times of the sprinter to cover a distance (100m, 200m, 400m etc) will differ. If you had no idea where the sprinter was running, or what the conditions were like, if the sprinter sets a certain time you can cross-correlate it with a certain time associated with certain surfaces. 

Benchmarking in computing works in a similar way, as it is a way of assessing the performance of a program or set of programs, and are designed to mimic a particular type of workload on a component or system. They can also be used to measure the differing performance across different systems. Usually codes can be tested on different computer architectures to see how a code performs. Like our sprinter, the times of benchmarks depends on a number of things, software, hardware or the computer itself and its architecture.

## Case study: Benchmarking with LAMMPS

With this new found knowledge on how benchmarking enables you to compare the performance of your computing system with some 'standard' systems, it helps you to know whether a further fine tuning of your job is required or not.

First, we will start with the simplest Lennard-Jones (LJ) system as provided in the 'bench' directory of the latest LAMMPS distribution. Following this, you will be given another example and you will follow the same set of exercises and compare your results with some 'known' benchmark.

> ## Run a LAMMPS job in a HPC
> Can you list the bare minimum files that you need to schedule a LAMMPS job in a HPC?
> > ## Solution
> > For running a LAMMPS job, we need;
> > 1. input file
> > 2. batch file
> > 
> > In general, each HPC uses a queueing system to manage all the jobs. Two such popular ones are PBS and Slurm. 
> >
> > Optional files include;
> > 1. Empirical potential file
> > 2. Data file
> > 
> > These optional files are only required when the empirical potential model parameters and the molecular coordinates are not defined within the LAMMPS input file.
> {: .solution}
{: .challenge}

The input file for the LJ-system is given below: 
```
{% include /snippets/ep02/in.lj %}
```
{: .bash}


The timing information for this run with both 1 and 4 processors is also provided with LAMMPS distribution. So, to benchmark it would be wise to run the same job with same processor settings. Let us now create a batch file to submit this job. 


> ## Editing a submission script for a LAMMPS job
>
> Here is shown the header of a job script to submit a LAMMPS job using 2 nodes and 48 processors. What modification is needed to submit the job using 4 processors?
>
> ```
> #!/bin/bash -x
> {{ site.sched_comment }} {{ site.sched_flag_account }}=myAccount
> {{ site.sched_comment }} {{ site.sched_flag_nodes }}=2
> {{ site.sched_comment }} {{ site.sched_flag_ntasks }}=24
> {{ site.sched_comment }} {{ site.sched_flag_out }}=mpi-out.%j
> {{ site.sched_comment }} {{ site.sched_flag_error }}=mpi-err.%j
> {{ site.sched_comment }} {{ site.sched_flag_time }}=00:05:00
> {{ site.sched_comment }} {{ site.sched_flag_partition }}=myQueue
>
> ... ... ...
> ... ... ...
> ```
> {: .bash}
> 
> > ## Solution
> > ```
> > {{ site.sched_comment }} {{ site.sched_flag_nodes }}=1
> > {{ site.sched_comment }} {{ site.sched_flag_ntasks }}=4
> > ```
> > {: .input}
> {: .solution}
{: .challenge}

The remainder of the file should now be used to set the LAMMPS environment variables and finally we need to invoke the LAMMPS executable for the run. In all modern HPCs, package specific environment variables are loaded or unloaded using modules. See below for an example code on how to use the `module` command to load LAMMPS for this course. Other modules aside from LAMMPS may be needed depending on your system.

```
{{ site.gpu_env }}
```
{: .source}

Now we'll invoke LAMMPS executable to do the job. This can be done using either;
```
{{ site.run_openmp }} {{ site.sched_lammps_exec }} < in.lj
```
{: .bash}

Or,
```
{{ site.run_mpi }} -np 1 {{ site.sched_lammps_exec }} < in.lj
```
{: .bash}

> ## Submission script: full view
>
> Create a file to submit a LAMMPS job for the above input file (in.lj) to 1 core only. You will submit the job to a partition/queue named `{{ site.sched_queue }}`. The job is expected to take less than 5 minutes.
>
> > ## Solution
> > ~~~
> > #!/bin/bash -x
> > {{ site.sched_comment }} {{ site.sched_flag_account }}=ecam
> > {{ site.sched_comment }} {{ site.sched_flag_nodes }}=1
> > {{ site.sched_comment }} {{ site.sched_flag_ntasks }}=1
> > {{ site.sched_comment }} {{ site.sched_flag_out }}=mpi-out.%j
> > {{ site.sched_comment }} {{ site.sched_flag_in }}=mpi-err.%j
> > {{ site.sched_comment }} {{ site.sched_flag_time }}=72:00:00
> > {{ site.sched_comment }} {{ site.sched_flag_partition }}={{ site.sched_queue }}
> >
> > {{ site.gpu_env }}
> >
> > {{ site.run_openmp }} {{ site.sched_lammps_exec }} < in.lj > out.lj
> > ~~~
> > {: .input}
> {: .solution}
{: .challenge}

## Understand the output files
Let us now look at the output files. Here, three files have been created: `log.lammps`, `mpi-out.xxxxx`, and `mpi-err.xxxxx`. Among these three, `mpi-out.xxxxx` is mainly to capture the screen output that have been generated during the job execution. The purpose of the `mpi-err.xxxxx` file is to log entries if there is any error occurring during run-time. The one that is created by LAMMPS is called `log.lammps`. 

Once you open `log.lammps`, you will notice that it contains most of the important information starting from the LAMMPS version, number of processors used for runs, processor lay out, thermodynamic steps, and timing. The header of a `log.lammps` file would be somewhat similar to this:
```
LAMMPS (18 Feb 2020)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:94)
using 1 OpenMP thread(s) per MPI task
```
{: .output}

Note that it tells you about the LAMMPS version, and `OMP_NUM_THREADS` which is one of the important environment variables required to set for obtaining a performance boost. This will be discussed at a later stage. But for now, we'll focus mainly on the timing information provided in this file.

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
{: .output}

Useful keywords to search for include:

  * **Loop time:** This shows the total wall-clock time for the simulation to run. (source: LAMMPS manual)
The following command can be used to extract this from `log.lammps`:

```
grep "Loop time" log.lammps| sed 's/|/ /' | awk '{print $4}'

$ 1.76553
```
{: .bash}

  * **Performance:** This is provided for convenience to help predict how long it will take to run a desired physical simulation. (source: LAMMPS manual)
Use the following command line to extract the value in units of `tau/day`:

```
grep "Performance" log.lammps| sed 's/|/ /' | awk '{print $2}'

$ 24468.549
```
{: .bash}

  * **CPU use:** This provides the CPU utilization per MPI task; it should be close to 100% times the number of OpenMP threads (or 1 of not using OpenMP). Lower numbers correspond to delays due to file I/O or insufficient thread utilization. (source: LAMMPS manual)
Use the following command line to extract the value in units of ```tau/day``` :

```
grep "CPU use" log.lammps| sed 's/|/ /' | awk '{print $1}'

$ 100.0%
```
{: .bash}

* **Timing Breakdown** Next, we'll discuss about the timing breakdown table for CPU runtime. If we try the following command;

```
grep -A 8 "breakdown" log.lammps 
```
{: .bash}

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
{: .output}

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
> Now submit a LAMMPS job for the above input file for a HPC that is available to you using both 1 and 4 processors. Extract the loop times for your runs and make a bar plot to see how the performance of your HPC for this particular job compares with LAMMPS standard benchmark and with the performance for two other HPCs.
> 
> | HPC system | 1 proc (sec) | 4 proc (sec) |
> |----------- | ------------ |------------- |
> | LAMMPS     | 2.26185      | 0.635957     |
> | HPC 1      | 2.24207      | 0.592148     |
> | HPC 2      | 1.76553      | 0.531145     |
> | HPC 3      |     ?        |     ?        |
> 
{: .challenge}
  
## Scaling

Scaling in computation is the effective use of resources. To explain this in more detail, lets head back to our chefs again from the previous episode

Let us assume that they are all bound by secrecy, and are not allowed to reveal to you what their craft is, pastry, meat, fish, soup, etc. You have to find out what their specialities are, what do you do? Do a test run and assign a chef to each course. Having a worker set to each task is all well and good, but there are certain combinations which work and some which do not, you might get away with your starter chef preparing a fish course, or your lamb chef switching to cook beef and vice versa, but you wouldn't put your pastry chef in charge of the main meat dish, you leave that to someone more qualified and better suited to the job. Eventually after a few test meals, you find out the best combination and you apply that to all your future meals.

Scaling in computing works in a similar way, thankfully not to that level of detail where one specific core is suited to one specific task, but finding the best combination is important and can hugely impact your code's performance. As ever with enhancing performance, you may have the resources, but the effective use of the resources is where the challenge lies. Having each chef cooking their specialised dishes would be good scaling, an effective use of your resources, but poor scaling is having your pastry chef doing the main dish, which is an ineffective use of resources.

**FIX ALL BELOW**

> ## Plotting performance and number of cores
> 
> Use the code template below to analyse how performance changes based on the setup (FIXME)
> 
> ```
> code
> ```
> What do you notice about this plot?
>
{: .challenge}

## How to perform a scaling analysis

(FIXME)

## Scaling data for LAMMPS run

(FIXME)

> ## Perform a scaling analysis
>
> Using the data given, run a simple LJ run for LAMMPS and perform a scaling analysis
>
> What is the speedup of the output?
{: .challenge}

{% include links.md %}
