---
title: "Benchmarking and Scaling"
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

To get a concept of what we mean by benchmarking, let's take the example of a sprint
athlete. The athlete runs a predetermined distance on a particular surface, and a time
is recorded. Based on different conditions, such as how dry or wet the surface is, or
what the surface is made of (grass, sand, or track) the times of the sprinter to cover
a distance (100m, 200m, 400m etc) will differ. If you know where the sprinter is
running, and what the conditions were like, when the sprinter sets a certain time you
can cross-correlate it with the known times associated with certain surfaces (our
**benchmarks**) to judge how well they are performing.

Benchmarking in computing works in a similar way, as it is a way of assessing the
performance of a program (or set of programs), and benchmark tests are designed to mimic
a particular type of workload on a component or system. They can also be used to measure
differing performance across different systems. Usually codes are tested on different
computer architectures to see how a code performs. Like our sprinter, the times of
benchmarks depends on a number of things: software, hardware or the computer itself and
it's architecture.

## Case study: Benchmarking with LAMMPS

As an example, let's create some benchmarks for you to compare the performance of some
'standard' systems. Using a 'standard' system is a good idea as a first attempt, since
we can measure our benchmarks against (published) information from others.  Knowing that
our installation is "sane" is a critical first step before we embark on generating **our
own benchmarks for our own use case**.

As an example, we will start with the simplest Lennard-Jones (LJ) system as provided in
the `bench` directory of the latest LAMMPS distribution. You will also be given another
example with which you can follow the same workflow and compare your results with some
'known' benchmark.

> ## Run a LAMMPS job in a HPC
> Can you list the bare minimum files that you need to schedule a LAMMPS job on an HPC
> system?
>
> > ## Solution
> > For running a LAMMPS job, we need;
> > 1. an input file
> > 2. a job submission file
> >
> >    In general, each HPC system uses a *resource manager* (frequently called
> >    *queueing system*) to manage all the jobs. Two popular ones are PBS and SLURM.
> >
> > Optional files include;
> > 1. Empirical potential file
> > 2. Data file
> >
> > These optional files are only required when the empirical potential model parameters
> > and the molecular coordinates are not defined within the LAMMPS input file.
> {: .solution}
{: .challenge}

The input file for the LJ-system is reproduced below:
```
{% include /snippets/ep02/in.lj %}
```
{: .bash}


The timing information for this run with both 1 and 4 processors is also provided with
the LAMMPS distribution. So, to benchmark it would be wise to run the same job with same
processor settings. Let us now create a batch file to submit this job.


> ## Editing a submission script for a LAMMPS job
>
> Here is shown the header of a job script to submit a LAMMPS job using 2 nodes and 48
> processors. What modification is needed to submit the job using 4 processors?
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

The remainder of the file should now be used to set any LAMMPS environment variables and
finally we need to invoke the LAMMPS executable for the run. In most modern HPC systems,
package specific environment variables are loaded or unloaded using *environment
modules* are the solution to these problems. A module is a self-contained description of
a software package - it contains the settings required to run a software package and,
usually, encodes required dependencies on other software packages. See below for an
example set of `module` commands to load LAMMPS for this course.

```
{{ site.gpu_env }}
```
{: .source}

Now we'll invoke LAMMPS executable to do the job. Since we are using a single CPU core,
we can either invoke LAMMPS directly with
```
{{ site.sched_lammps_exec }} < in.lj
```
{: .bash}

or through our *MPI runtime*
```
{{ site.run_mpi }} {{ site.mpi_runtime_single_core_flags }} {{ site.sched_lammps_exec }} < in.lj
```
{: .bash}

Let's use the MPI runtime version so that we can easily change it to use 4 cores.

> ## Submission script: full view
>
> Create a file to submit a LAMMPS job for the above input file (`in.lj`) to 1 core
> only. You will submit the job to a partition/queue named `{{ site.sched_queue }}`. The
> job is expected to take less than 5 minutes.
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
> > {{ site.run_mpi }} {{ site.sched_lammps_exec }} < in.lj > out.lj
> > ~~~
> > {: .input}
> {: .solution}
{: .challenge}

## Understand the output files

Let us now look at the output files. Here, three files have been created: `log.lammps`,
`mpi-out.xxxxx`, and `mpi-err.xxxxx`. Among these three, `mpi-out.xxxxx` is mainly to
capture the screen output that have been generated during the job execution. The purpose
of the `mpi-err.xxxxx` file is to log entries if there is any error occurring during
run-time. The one that is created by LAMMPS is called `log.lammps`.

Once you open `log.lammps`, you will notice that it contains most of the important
information starting from the LAMMPS version, number of processors used for runs,
processor lay out, thermodynamic steps, and timing. The header of a `log.lammps` file
should be somewhat similar to this:
```
LAMMPS (18 Feb 2020)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:94)
using 1 OpenMP thread(s) per MPI task
```
{: .output}

Note that it tells you about the LAMMPS version, and `OMP_NUM_THREADS` which is one of
the important environment variables required to set for obtaining a performance boost.
This will be discussed at a later stage. But for now, we'll focus mainly on the timing
information provided in this file.

When the run concludes, LAMMPS prints the final thermodynamic state and a total run time
for the simulation. It also appends statistics about the CPU time and storage
requirements for the simulation. An example set of statistics is shown here:

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

  * **`Loop time:`** This shows the total wall-clock time for the simulation to run.
    (source: LAMMPS manual)

    The following command can be used to extract this the relevant line from
    `log.lammps`:

    ```
    grep "Loop time" log.lammps
    ```
    {: .bash}

  * **Performance:** This is provided for convenience to help predict how long it will
    take to run a desired physical simulation. (source: LAMMPS manual)

    Use the following command line to extract line (we will use the value in units of
    `tau/day`):

    ```
    grep "Performance" log.lammps
    ```
    {: .bash}

  * **CPU use:** This provides the CPU utilization per MPI task; it should be close to
    100% times the number of OpenMP threads (or 1 of not using OpenMP). Lower numbers
    correspond to delays due to file I/O or insufficient thread utilization. (source:
    LAMMPS manual)

    Use the following command line to extract the relevant line:

    ```
    grep "CPU use" log.lammps
    ```
    {: .bash}

  * **Timing Breakdown** Next, we'll discuss about the timing breakdown table for CPU
    runtime. If we try the following command;

    ```
    # extract 8 lines after the occurrence of the "breakdown"
    grep -A 8 "breakdown" log.lammps
    ```
    {: .bash}

    you should see output similar to the following:

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

    The above table shows the times taken by the major categories of a LAMMPS run. A
    brief description of these categories has been provided in
    [LAMMPS manual](https://lammps.sandia.gov/doc/Run_output.html):

    * Pair = non-bonded force computations
    * Bond = bonded interactions: bonds, angles, dihedrals, impropers
    * Kspace = long-range interactions: Ewald, PPPM, MSM
    * Neigh = neighbor list construction
    * Comm = inter-processor communication of atoms and their properties
    * Output = output of thermodynamic info and dump files
    * Modify = fixes and computes invoked by fixes
    * Other = all the remaining time

    This is very useful in the sense that it helps you to identify the where you spend
    most of your computing time (and so help you know what you should be targeting)! It
    will discussed later in more detail.

> ## Now run a benchmark...
>
> Now submit a LAMMPS job for the above input file using both 1 and 4 processors.
> Extract the loop times for your runs and see how the for this particular job compares
> with LAMMPS standard benchmark and with the performance for two other HPC systems.
>
> | HPC system | 1 proc (sec) | 4 proc (sec) |
> |----------- | ------------ |------------- |
> | LAMMPS     | 2.26185      | 0.635957     |
> | HPC 1      | 2.24207      | 0.592148     |
> | HPC 2      | 1.76553      | 0.531145     |
> | MY HPC     |     ?        |     ?        |
>
> Why might these results differ?
>
{: .challenge}

## Scaling

Scaling behaviour in computation is centred around the effective use of resources as you
scale up the amount of computing resources you use. An example of "good" scaling would
be that when we use twice as many CPUs, we get an answer in half the time. "Bad" scaling
would be when the answer takes only 10% less time when we double the CPUs. This example
is one of **strong scaling**, where the workload doesn't change as we increase our
scaling.

For **weak scaling**, we want to increase our workload without increasing our walltime,
and we do that by using additional resources. To look at this in more detail, let's head
back to our chefs again from the previous episode, where we had more courses to serve
but the same amount of time to do it in.

Let us assume that they are all bound by secrecy, and are not allowed to reveal to you
what their craft is, pastry, meat, fish, soup, etc. You have to find out what their
specialities are, what do you do? Do a test run and assign a chef to each course. Having
a worker set to each task is all well and good, but there are certain combinations which
work and some which do not, you might get away with your starter chef preparing a fish
course, or your lamb chef switching to cook beef and vice versa, but you wouldn't put
your pastry chef in charge of the main meat dish, you leave that to someone more
qualified and better suited to the job. Eventually after a few test meals, you find out
the best combination and you apply that to all your future meals.

Scaling in computing works in a similar way, thankfully not to that level of detail
where one specific core is suited to one specific task, but finding the best combination
is important and can hugely impact your code's performance. As ever with enhancing
performance, you may have the resources, but the effective use of the resources is
where the challenge lies. Having each chef cooking their specialised dishes would be
good weak scaling: an effective use of your resources. Poor weak scaling would result
from having your pastry chef doing the main dish, which is an ineffective use of
resources.

**FIX ALL BELOW - do a simple scaling analysis for a full node and 2 nodes, and compare
it with the results for 1 and 4 cores**

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
