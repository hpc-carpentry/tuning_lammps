---
title: "Benchmarking and Scaling"
teaching: 15
exercises: 15
questions:
- "What is benchmarking?"
- "How do I do a benchmark?"
- "What is scaling?"
- "How do I perform a scaling analysis?"
objectives:
- "Be able to perform a benchmark analysis of an application"
- "Be able to perform a scaling analysis of an application"
keypoints:
- "Benchmarking is a way of assessing the performance of a program or set of programs"
- "The `log.lammps` file shows important information about the timing, processor layout, etc.
  which you can use to record your benchmark"
- "Scaling concerns the effective use of computational resources. Two types are typically discussed:
  strong scaling (where we increase the compute resources but keep the problem size the same) and
  weak scaling (where we increase the problem size in proportion to our increase of compute
  resources"
---

## What is benchmarking?

To get an idea of what we mean by benchmarking, let's take the example of a sprint
athlete. The athlete runs a predetermined distance on a particular surface, and a time
is recorded. Based on different conditions, such as how dry or wet the surface is, or
what the surface is made of (grass, sand, or track) the times of the sprinter to cover
a distance (100m, 200m, 400m etc) will differ. If you know where the sprinter is
running, and what the conditions were like, when the sprinter sets a certain time you
can cross-correlate it with the known times associated with certain surfaces (our
**benchmarks**) to judge how well they are performing.

Benchmarking in computing works in a similar way: it is a way of assessing the
performance of a program (or set of programs), and benchmark tests are designed to mimic
a particular type of workload on a component or system. They can also be used to measure
differing performance across different systems. Usually codes are tested on different
computer architectures to see how a code performs on each one. Like our sprinter, the times of
benchmarks depends on a number of things: software, hardware or the computer itself and
it's architecture.

## Case study: Benchmarking with LAMMPS

As an example, let's create some benchmarks for you to compare the performance of some
'standard' systems in LAMMPS. Using a 'standard' system is a good idea as a first attempt, since
we can measure our benchmarks against (published) information from others.  Knowing that
our installation is "sane" is a critical first step before we embark on generating **our
own benchmarks for our own use case**.

> ## Installing your own software vs. system-wide installations
>
> Whenever you get access to an HPC system, there are usually two ways to get access to
> software: either you use a system-wide installation or you install it yourself. For widely
> used applications, it is likely that you should be able to find a system-wide installation.
> In many
> cases using the system-wide installation is the better option since the system
> administrators will (hopefully) have configured the application to run optimally for
> that system. If you can't easily find your application, contact user support for the
> system to help you.
>
> You should still check the benchmark case though! Sometimes administrators are short
> on time or background knowledge of applications and do not do thorough testing.
{: .callout}

As an example, we will start with the simplest Lennard-Jones (LJ) system as provided in
the `bench` directory of the LAMMPS distribution. You will also be given another
example with which you can follow the same workflow and compare your results with some
'known' benchmark.

> ## Running a LAMMPS job on an HPC system
>
> Can you list the bare minimum files that you need to schedule a LAMMPS job on an HPC
> system?
>
> > ## Solution
> > For running a LAMMPS job, we need:
> > 1. an input file
> > 2. a job submission file - in general, each HPC system uses a *resource manager*
> >    (frequently called *queueing system*) to manage all the jobs. Two popular ones
> >    are PBS and SLURM.
> >
> > Optional files include:
> > 1. Empirical potential file
> > 2. Data file
> >
> > These optional files are only required when the empirical potential model parameters
> > and the molecular coordinates are not defined within the LAMMPS input file.
> {: .solution}
{: .challenge}

The input file we need for the LJ-system is reproduced below:
~~~
{% include {{ site.snippets }}/ep03/in.lj %}
~~~
{: .source}

The timing information for this run with both 1 and 4 processors is also provided with
the LAMMPS distribution. To do an initial benchmark our installation it would be wise to
run the test case with the same number of processors in order to compare with the timing
information provided by LAMMPS.

Let us now create a job file (sometimes called a batch file) to submit a job for a larger
test case. Writing
a job file from scratch is error prone. Many computing sites offer a number of
example job scripts to let you get started. We'll do the same and provide you with an example
, but created specifically for our LAMMPS use case.

First we need to tell the batch system what resources we need:
~~~
{% include {{ site.snippets }}/ep03/job_resources_2nodeMPI.snip %}
~~~
{: .source}
in this case, we've asked for all the cores on 2 nodes of the system for 5 minutes.

Next we should tell it about the environment we need to run in. In most modern HPC systems,
package specific environment variables are loaded or unloaded using *environment
modules*. A module is a self-contained description of
a software package - it contains the settings required to run a software package and,
usually, encodes required dependencies on other software packages. See below for an
example set of `module` commands to load LAMMPS for this course:
~~~
{% include {{ site.snippets }}/ep03/job_environment_lammps.snip %}
~~~
{: .language-bash}

And finally we tell it how to actually run the LAMMPS executable on the system.
If we were using a single CPU core, we can invoke LAMMPS directly with
~~~
{{ site.lammps.exec }} -in in.lj
~~~
{: .language-bash}
but in our case we are interested in using the MPI runtime across 2 nodes. On our system
we will use the {{ site.mpi_runtime.implementation }} MPI implementation using
`{{ site.mpi_runtime.launcher }}` to launch the MPI processes. Let's see how that looks
like for our current use case (with `in.lj` as the input file):
~~~
{% include {{ site.snippets }}/ep03/job_execution_2nodeMPI.snip %}
~~~
{: .language-bash}

Now let's put all that together to make our job script:
~~~
{% include {{ site.snippets }}/ep03/job_resources_2nodeMPI.snip %}
{% include {{ site.snippets }}/ep03/job_environment_lammps.snip %}
{% include {{ site.snippets }}/ep03/job_execution_2nodeMPI.snip %}
~~~
{: .language-bash}

> ## Edit a submission script for a LAMMPS job
>
> Duplicate the job script we just created so that we have versions that will run on
> 1 core and 4 cores.
>
> Make a new directories (called `4core_lj` and `1core_lj`) and for each directory *copy*
> inside your input file and the relevant job script. For each case, enter that directory
> (so that all output from your job is stored in the same place) and run the job script on
> {{ site.remote.name }}.
>
> > ## Solution
> > Our single core version is
> > {% capture mycode %}{% include {{ site.snippets }}/ep03/1core_job_script %}{% endcapture %}
> > {% assign lines_of_code = mycode | strip |newline_to_br | strip_newlines | split: "<br />" %}
> > ~~~{% for member in lines_of_code %}
> > {{ member }}{% endfor %}
> > ~~~
> > {: .language-bash}
> > and our 4 core version is
> > {% capture mycode %}{% include {{ site.snippets }}/ep03/4core_job_script %}{% endcapture %}
> > {% assign lines_of_code = mycode | strip |newline_to_br | strip_newlines | split: "<br />" %}
> > ~~~{% for member in lines_of_code %}
> > {{ member }}{% endfor %}
> > ~~~
> > {: .language-bash}
> {: .solution}
{: .challenge}

### Understanding the output files

Let us now look at the output files. Here, three files have been created: `log.lammps`,
`mpi-out.xxxxx`, and `mpi-err.xxxxx`. Among these three, `mpi-out.xxxxx` is mainly to
capture the screen output that would have been generated during the job execution. The purpose
of the `mpi-err.xxxxx` file is to log entries if there is any error (and sometimes other
information) that occurred during
run-time. The one that is created by LAMMPS is called `log.lammps`. Note that LAMMPS
overwrites the default `log.lammps` file with every execution, but the information we
are concerned with there is also stored in our `mpi-out.xxxxx` file.

Once you open `log.lammps`, you will notice that it contains most of the important
information starting from the LAMMPS version (in our case we are using
`{{ site.lammps.version }}`), the number of processors used for runs,
the processor lay out, thermodynamic steps, and some timings. The header of your
`log.lammps` file
should be somewhat similar to this:
~~~
LAMMPS (18 Feb 2020)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:94)
using 1 OpenMP thread(s) per MPI task
~~~
{: .output}

Note that it tells you about the LAMMPS version, and `OMP_NUM_THREADS` which is one of
the important environment variables we need to know about to leverage OpenMP. For
now, we'll focus mainly on the timing
information provided in this file.

When the run concludes, LAMMPS prints the final thermodynamic state and a total run time
for the simulation. It also appends statistics about the CPU time and storage
requirements for the simulation. An example set of statistics is shown here:

~~~
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
~~~
{: .output}

Useful keywords to search for include:

  * **`Loop time:`** This shows the total wall-clock time for the simulation to run.
    (source: LAMMPS manual)

    The following command can be used to extract this the relevant line from
    `log.lammps`:

    ~~~
    grep "Loop time" log.lammps
    ~~~
    {: .language-bash}

  * **Performance:** This is provided for convenience to help predict how long it will
    take to run a desired physical simulation. (source:
    [LAMMPS manual](https://lammps.sandia.gov/doc/Manual.html))

    Use the following command line to extract line (we will use the value in units of
    `tau/day`):

    ~~~
    grep "Performance" log.lammps
    ~~~
    {: .language-bash}

  * **CPU use:** This provides the CPU utilization per MPI task; it should be close to
    100% times the number of OpenMP threads (or 1 of not using OpenMP). Lower numbers
    correspond to delays due to file I/O or insufficient thread utilization. (source:
    [LAMMPS manual](https://lammps.sandia.gov/doc/Manual.html))

    Use the following command line to extract the relevant line:

    ~~~
    grep "CPU use" log.lammps
    ~~~
    {: .language-bash}

  * **Timing Breakdown** Next, we'll discuss about the timing breakdown table for CPU
    runtime. If we try the following command;

    ~~~
    # extract 8 lines after the occurrence of the "breakdown"
    grep -A 8 "breakdown" log.lammps
    ~~~
    {: .language-bash}

    you should see output similar to the following:

    ~~~
    MPI task timing breakdown:
    Section |  min time  |  avg time  |  max time  |%varavg| %total
    ---------------------------------------------------------------
    Pair    | 1.5244     | 1.5244     | 1.5244     |   0.0 | 86.34
    Neigh   | 0.19543    | 0.19543    | 0.19543    |   0.0 | 11.07
    Comm    | 0.016556   | 0.016556   | 0.016556   |   0.0 |  0.94
    Output  | 7.2241e-05 | 7.2241e-05 | 7.2241e-05 |   0.0 |  0.00
    Modify  | 0.023852   | 0.023852   | 0.023852   |   0.0 |  1.35
    Other   |            | 0.005199   |            |       |  0.29
    ~~~
    {: .output}

    The above table shows the times taken by the major categories of a LAMMPS run. A
    brief description of these categories has been provided in the
    [run output section of the LAMMPS manual](https://lammps.sandia.gov/doc/Run_output.html):

    * Pair = non-bonded force computations
    * Bond = bonded interactions: bonds, angles, dihedrals, impropers
    * Kspace = long-range interactions: Ewald, PPPM, MSM
    * Neigh = neighbor list construction
    * Comm = inter-processor communication of atoms and their properties
    * Output = output of thermodynamic info and dump files
    * Modify = fixes and computes invoked by fixes
    * Other = all the remaining time

    This is very useful in the sense that it helps you to identify where you spend
    most of your computing time (and so help you know what you should be targeting)! It
    will discussed later in more detail.

> ## Now run a benchmark...
>
> From the jobs that you ran previously,
> extract the loop times for your runs and see how they compare
> with the LAMMPS standard benchmark and with the performance for two other HPC systems.
>
> | HPC system | 1 core (sec) | 4 core (sec) |
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
scale up the amount of computing resources you use. An example of "perfect" scaling would
be that when we use twice as many CPUs, we get an answer in half the time. "Bad" scaling
would be when the answer takes only 10% less time when we double the CPUs. This example
is one of **strong scaling**, where the workload doesn't change as we increase our
resources.

> ## Plotting strong scalability
>
> Use the original job script for 2 nodes and run it on {{ site.remote.name }}.
>
> Now that
> you have results for 1 core, 4 cores and 2 nodes, create a *scalability plot* with
> the number of CPU cores on the X-axis and the loop times on the Y-axis (use your
> favourite plotting tool, an online plotter or even pen and paper).
>
> Are you close to "perfect" scalability?
>
{: .challenge}

### Weak scaling

For **weak scaling**, we want usually want to increase our workload without increasing
our *walltime*,
and we do that by using additional resources. To consider this in more detail, let's head
back to our chefs again from the previous episode, where we had more people to serve
but the same amount of time to do it in.

We hired extra chefs who have specialisations but let us assume that they are all bound
by secrecy, and are not allowed to reveal to you
what their craft is, pastry, meat, fish, soup, etc. You have to find out what their
specialities are, what do you do? Do a test run and assign a chef to each course. Having
a worker set to each task is all well and good, but there are certain combinations which
work and some which do not, you might get away with your starter chef preparing a fish
course, or your lamb chef switching to cook beef and vice versa, but you wouldn't put
your pastry chef in charge of the main meat dish, you leave that to someone more
qualified and better suited to the job.

Scaling in computing works in a similar way, thankfully not to that level of detail
where one specific core is suited to one specific task, but finding the best combination
is important and can hugely impact your code's performance. As ever with enhancing
performance, you may have the resources, but the effective use of the resources is
where the challenge lies. Having each chef cooking their specialised dishes would be
good weak scaling: an effective use of your additional resources. Poor weak scaling
will likely result from having your pastry chef doing the main dish.
