---
title: "Accelerating LAMMPS"
teaching: 0
exercises: 0
questions:
- "What are the various options to accelerate LAMMPS"
- "What hardwares can LAMMPS be used on?"
- "How can I enable architecture support at runtime?"
- "What accelerator packages are compatible with which hardware?"
- "What is KOKKOS and why should I use it?"
objectives:
- "First learning objective. (FIXME)"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---
## How can I accelerate LAMMPS performance?

There are two basic approaches to speed-up LAMMPS. One is to use better algorithms for certain 
types of calculation, and the other is to use highly optimized codes via various "accelerator 
packages" deviced for hardware specific platforms.

One popular example of the first approach is to use the Wolf summation method instead of the Ewald
summation method for calculating long range Coulomb interactions effectively using a short-range
potential. Similarly there are a few FFT schemes offered by LAMMPS and a user has to make a 
trade-off between accuracy and performance depending on their computational needs. This lesson is
not aimed to discuss such types of algorithm based speed-up of LAMMPS, instead we'll focus on a few
accelerator packages that is used to extract the most out of the available hardware of a HPC system.

There are five accelerator packages currently offered by LAMMPS. These are;

1. **OPT**
2. **USER-INTEL**
3. **USER-OMP**
4. **GPU**
5. **Kokkos**

Specialized codes contained in these packages help LAMMPS to perform well on modern HPC platforms
which could have different hardware partitions. Therefore, the very next question that arises that
what are these hardwares that are supported by these packages?

> ## Supported hardwares
>
> | Hardware        | Accelerators                      |
> | --------------- | --------------------------------- |
> | Multi-core CPUs | OPT, USER-INTEL, USER-OMP, Kokkos |
> | Intel Xeon Phi  | USER-INTEL, Kokkos                |
> | NVIDIA GPU      | GPU, Kokkos                       |
>
{: .callout}

Within the limited scope of this tutorial, this is almost impossible to discuss all of the above
packages here in detail. The key point to understand is that the acceleration is achieved by
multithreading either through OpenMP or GPU. The **ONLY** accelerator package that supports both
kinds of hardwares is **Kokkos**. Kokkos is a templated C++ library developed in Sandia National
Laboratory and this helps to create an abstraction that allows a *single implementation* of a
software application on different kinds of hardwares by simply mapping C++ kernel onto various
backend languages. This will be discussed more later in the
[next lesson]({{page.root}}/06-invoking-kokkos).

In the meantime, we'll touch a few key points about other accelerator packages to give you a feel
about what these packages offer, to learn to invoke an accelerator package in a LAMMPS run, and get some data to comapre the sppedup with regular as well as Kokkos-enabled LAMMPS runs. 

## OPT package

* Acceleration, in this case, is achieved by using templeted C++ library to reduce computational
  overheads due to `if` tests and other conditional code blocks.
* This also provides better vectorization operations as compared to its regular CPU version.
* Only a handful of pair styles can be accelerated using this package, which can be found
  [here]({{page.root}}/reference/#package-OPT).
* This generally offers 5-20% savings on computational cost on most of the machines

> ## Effect on timing breakdown table
>
> We have discussed earlier that at the end of each run LAMMPS prints a timing breakdown table
> where it categorises the spent time into several categories like *Pair*, *Bond*, *Kspace*,
> *Neigh*, *Comm*, *Output*, *Modify*, *Other*. Can you make a justified guess about which of
> these category could be affected by the use of the *OPT* package?
> >
> > ## Solution
> >
> > The *Pair* component will see a reduction in cost since this accelerator package aims to work
> > on the pair styles only.
> {: .solution}
{: .discussion}

## USER-INTEL package

The USER-INTEL package supports *single*, *double* and *mixed* precision calculations. 
Acceleration, in this case, is achieved in two different ways.

* Use vectorisation on multi-core CPUs
* Offload calculations of neighbour list and non-bonded interactions to Phi co-processors.

There are, however, a number of conditions;

* For using the offload feature, the Intel Xeon Phi coprocessors are required.
* For using vectorization feature, Intel compiler with version 14.0.1.106 or versions 15.0.2.044
  and higher is required on both multi-core CPUs and Phi systems.

There are many LAMMPS features that are supported by this accelerator package, which can be found
[here]({{page.root}}/reference/#package-USER-INTEL).

Performance enhancement using this package depends on many considerations, such as the hardware that is available to you, various styles that you are using in the input, the size of your problem, and precision. For example, if you are using a pair style (say, `reax`) for which this is not implemented, its obvious that you are not going to have a performance gain for the *Pair* part of the calculation. Now, if the majority of the computation time is coming from the *Pair* part then you are in trouble. If you would like to know how much speedup you can achieve using USER-INTEL, you can look [here](https://lammps.sandia.gov/doc/Speed_intel.html)

## USER-OMP package

This accelerator package offers performance gain through otimisation and multi-threading via OpenMP interface. In order to make the multi-threading functional, you need multi-core CPUs and a compiler that supports multithreading. If your compiler does not support multithreading then also you can use it as an optimized serial code. Considerably a big sub-set of the LAMMPS routines can be used with this accelerator.

A list of functionalities enabled with this package can be found
[here]({{page.root}}/reference/#package-USER-OMP).

Generally, one can expect 5-20% performance when using this package either in serial or parallel. The optimal number of OpenMP threads to use is to be always tested for a problem. But, this gives better performance when used for less number of threads, generally 2-4. It is important to remember that MPI implementation in LAMMPS is so robust that you may always expect this to be more effective than using OpenMP on multi-core CPUs.

Let us now come back to the *Rhodopsin* example for which we did a thorough scaling study in the previous episode. We found that the *Kspace* and *Neigh* calculations suffer fron poor scalability as you increase number of cores to do the calculations. In such situation a hybrid approach combining parallelizing over domains (i.e. MPI-based) and parallelizing over atoms (i.e. thread based OpenMP) could be more beneficial to improve scalability than a pure MPI-based approach. To test this, in the following exercise, we'll do a set of calculations to mix MPI and OpenMP using the USER-OMP package. Additionally, this exercise will also help us to learn the basic principles of invoking accelerator packages in a LAMMPS run. Before strating our runs, let us now discuss the syntax of the *package* command in LAMMPS, as outlined below. 

## How to invoke a package in LAMMPS run?
To call an accelerator packages (USER-INTEL, USER-OMP, GPU, KOKKOS) in your LAMMPS run, you need to know a LAMMPS command called `package`. This command invokes package-specific settings for an accelerator. You can learn about this command in detail from the
[LAMMPS manual](https://lammps.sandia.gov/doc/package.html).

The basic syntax of this command is:
*package style args keywords values*

```style``` provides you to choose the accelerator package for your run. There are four different
packages available currently (version 3Mar20):

* `gpu`: This calls the *GPU* package
* `intel`: This calls the *USER-INTEL* package
* `omp` : This calls the *USER-OMP* package
* `kokkos`: This calls the *Kokkos* package

## How to invoke the USER-OMP package?
There are two alternate ways to fo this, either you can edit the LAMMPS input file to add the extra 'stuffs' corresponsing to the *package* command, or invoke it through command-line keeping the input files unchanged.

If the `package` command is specified in an input script, it must be near the top of the script, before the simulation box has been defined. This is because it specifies settings that the accelerator packages use in their initialization, before a simulation is defined. This command can be used in LAMMPS in two different ways:

* Edit the input file and introduce the line comprising the *package* command in it. This is perfectly fine, but always remember to use this near the top of the script, before the simulation box has been defined. This is because it specifies settings that the accelerator packages use in their initialization, before a simulation is defined. 

To call *USER-OMP* in a LAMMPS run, use *omp* as *style*. Next you need to choose proper *arguments* for the *omp* style. *Argument* should be chosen as the number of OpenMP threads that you like to associate with each MPI process. This is an integer and should be chosen sensibly. If you have N number of physical cores available per node then *Number of MPI processes* x *Number of OpenMP threads* = *Number of cores per node*.

Each *argument* comes with a number of *keyword* and their corresponding *values*. These *keyword/values* provides you enhanced flexibility to distribute your job among the MPI ranks and threads. For a quick reference, the following table could be useful: 

|Keyword   | values  | What it does? |
|----------|---------|---------------|
| neigh    | yes     | threaded neighbor list build (this is the default) |
| neigh    | no      | non-threaded neighbor list build |

An example of calling the *USER-OMP* package in a LAMMPS input file is given below:

```
package omp 4 neigh no
```
{: .bash}

Additionally, you also need to append an extra "/omp" suffix wherever applicable. For example, a pair potential with USER-OMP optimization should be mentioned in the input file as:

```
pair_style      lj/charmm/coul/long/omp 8.0 10.0
```
{: .bash}

* A simpler way to do this is through the command-line when launching LAMMPS using the `-pk`command-line switch. The syntax would be exactly the same as when used in an input script:

```
export OMP_NUM_THREADS=4
export OMP_PROC_BIND=spread
export OMP_PLACES=threads
mpirun -np 10 -ppn 10 lmp -sf omp -pk omp 4 -in in.rhodo neigh no
```
{: .bash}

The second method appears to be convenient since you don't need to take the hassle to edit the input file (and possibly in many places)!

Note that there is an extra command-line switch in the above command-line. Do you know what thisis for? To distinguish the various styles of these accelerator packages from its 'regular' non-accelerated variants, LAMMPS has introduces suffixes and the `-sf` switch  auto-appends these accelerator suffixes to various styles in the input script. Therefore, when an accelerator package is invoked through the `-pk` switch (for example, `-pk omp` or `-pk gpu`), the `-sf` switch ensures that the appropriate style is also being invoked in the simulation (for example, it ensures that the `lj/cut/gpu` is used instead of `lj/cut` as `pair_style`, or,  `lj/charmm/coul/long/omp` is used in place of `lj/charmm/coul/long`).  

In this tutorial, we'll stick to the second method of invoking the accelerator package, i.e. through the command-line.

## Case study: Rhodopsin (with USER-OMP package)
We shall use the same input file for the rhodopsin system with lipid bilayer. The MD settings for this run is described in Episode 2. In this episode, we'll run this using the USER-OMP package to mix MPI and OpenMP. For all the runs use the default value for the *neigh* keyword. 

1. First, find out the number of cpu cores available per node in the HPC system that you are using and then figure out all the possible MPI/OpenMP combinations that you can have per node. For example, I did this study in Intel Xeon Gold 6148 (Skylake) processor with 2x20 core 2.4 GHz having 192 GiB of RAM. This means each node has 40 physical cores. So, to satify the relation, *Number of MPI processes* x *Number of OpenMP threads* = *Number of cores per node*, I can have the following combinations per node: 1MPI/40 OpenMP threads, 2MPI/20 OpenMP threads, 4MPI/10 OpenMP threads, 5MPI/8 OpenMP threads, 8MPI/5 OpenMP threads, 10MPI/4 OpenMP threads, 20MPI/2 OpenMP threads, and 40MPI/1 OpenMP threads. I like to see scaling, say up to 10 nodes or more. This means that I have to run a total 80 calculations for 10 nodes since I have 8 MPI/OpenMP combinations for each node. Run the jobs for all possible combination in your HPC system.
2. Run the job for with pure-MPI settings, i.e. with 40 cores (1node), 80 cores (2 nodes), and so on and make sure not to use any OpenMP threading in these runs.
3. A good metric to measure scalability is to compute *parallel efficiency* for each of these runs. *Parallel efficiency* is defined as:
  *Parallel efficiency = (1/Np) * (Time taken by a serial run / ( Time taken by Np processors)*
Calculate *parallel efficiency* for each of these jobs. To get the total time taken by each job, search for "wall time" in the log/screen output files.
4. Make a plot of *parallel efficiency* versus *number of nodes*.
5. Write down your observation and make comments on any performance enhancement when you compare these results with the pure MPI runs.

### Solution
For a perfectly scalable system, parallel efficiency should be qual to 100%, and as it approaches zero we say that the paralle performance is poor.
A few observations from the following plot:
1. As we increase number of nodes, the parallel efficiency decreases considerably for all the runs. This decrease in performance could be associated to the poor scalability of the *Kspace* and *Neigh* computations. We have discussed about this in episode 2.
2. Parallel efficency is increased by about 10-15% when we use mixed MPI+OpenMP approach.
3. The performance of hybrid runs are better than or comparable to pure MPI runs only when the number of OpenMP threads are less than or equals to five. This implies that USER-OMP package shows scalability only when number of threads are less in number.
4. Though we are seeing about 10-15% increase in parallel efficiency of hybrid MPI+OpenMP runs (using 2 threads) over pure MPI runs, still it is important to note that trends in loss of performance with increasing core number is similar in both of these types of runs thus indicating that this increase in performance might not be due to threading but rather due to better SIMD vectorization. Specially, for Skylake processor the vectorization capability is great.  In fact, in LAMMPS, MPI-based parallelization almost always win over OpenMP until thousands of MPI ranks are being used where communication overheads very much significant. There are overheads to making the kernels thread-safe. 

![scaling_rhodo_user_omp](../fig/05/scaling_rhodo_user_omp.png)

## GPU package

Using the GPU package in LAMMPS, one can achieve performance gain by coupling GPUs to one or many
CPUS. It provides supports for both NVIDIA and OpenCL and thus it helps to port GPU acceleration
to variety of hardwares. This becomes possible since the codes in GPU packages call the generic GPU
libraries present in the lib/gpu folder.

Calculations that require access to atomic data like coordinates, velocities, forces may suffer
bottlenecks since at every step these data are communicated back and forth between CPUs and GPUs.
Calculations can be done in single, double or mixed precisions.

In case of GPU packages, computations are shared between CPU and GPU unlike the Kokkos(GPU) package
where the primary aim is to offload all of the calculations to the GPUs only. For example,
asynchronous force calculations like **pair** vs **bond/angle/dihedral/improper** can be done
simultaneously on GPUs and CPUs respectively. Similarly, for PPPM calculations the charge
assignment and the force computations are done on GPUs whereas the FFT calculations that require
MPI communications are done on CPUs. Neighbour lists can be built on either CPUs or GPUs. You can
control this using specific flags in the command line of your job submission script. Thus GPU
package provides a balanced mix of GPU and CPU usage for a particular simulation to achieve a
performance gain.

A list of functionalities enabled with this package can be found
[here]({{page.root}}/reference/#package-GPU).

A question that you may be asking is how much speed-up would you expect from the GPU package.
Unfortunately there is no 'one-line' answer for this. This can depend on many things starting from
the hardware specification to the complexities involved with a specific problem that you are
simulating. However, for a given problem one can always optimize the run-time parameters to extract
most out of a hardware. In the following section, we'll discuss some of these tuning parameters for
the simplest LJ-systems.

The primary aim for this following exercise is:

* To get familiar with the methodology of calling an accelerator package in a LAMMPS run
* To get a primary understanding of the various commandline arguments that can control how a job is
  distributed among cpus/gpus, how to control cpu/gpu communications, etc. etc.
* To get an initial idea on how to play with different run-time parameters to get an optimum
  performance.
* Finally, one can also make a fair comparison of performance between a *regular* LAMMPS run, the
  GPU package and a Kokkos implementation of GPU functionality.
* Moreover, this exercise will also help the users to extend the knowledge of using the *package*
  command so that they can figure out by themselves how to use other accelerator packages in LAMMPS.

Before invoking the GPU package, you must ask the following questions:

 1. Do I have an access to a computing node having a GPU?
 2. Is my LAMMPS binary is built with GPU package?

If the answer to these two questions is a *yes* then we you can proceed to the following section.

## How to invoke the GPU package in LAMMPS run?

As discussed above, you need to use the *package* command to invoke the *GPU* package. To use *GPU package* as an accelerator you need to select `gpu` as *style*. Next you need to choose proper *arguments* for the *gpu* style. The argument for *gpu* style is *ngpu*.

* `ngpu`: This sets the number of GPUs per node. There must be at least as many MPI tasks per node
  as GPUs, as set by the mpirun or mpiexec command. If there are more MPI tasks (per node) than GPUs,
  multiple MPI tasks will share each GPU.

Each *argument* comes with a number of *keyword* and their corresponding *values*. These 
*keyword/values* provides you enhanced flexibility to distribute your job among CPUs and GPUs in an
optimum way. For a quick reference, the following table could be useful:

> ## Packages in LAMMPS; Keywords
>
> | Keywords   |Use                                                                                                           |Default value |
> |------------|--------------------------------------------------------------------------------------------------------------|--------------|
> |`neigh`     | specifies where neighbor lists for pair style computation will be built: GPU or CPU                          | yes          |
> |`newton`    | sets the Newton flags for pairwise (not bonded) interactions to off or on                                    | off          |
> |`binsize`   | sets the size of bins used to bin atoms in neighbor list builds performed on the GPU, if neigh = yes is set  | 0.0          |
> |`split`     | used for load balancing force calculations between CPU and GPU cores in GPU-enabled pair styles              |              |
> |`gpuID`     | allows selection of which GPUs on each node will be used for a simulation                                    |              |
> |`tpa`       | sets the number of GPU thread per atom used to perform force calculations                                    | 1            |
> |`device`    | used to tune parameters optimized for a specific accelerator and platform when using OpenCL                  |              |
> |`blocksize` | allows you to tweak the number of threads used per thread block                                              | minimum = 32 |
>
{: .callout}

## How to invoke the GPU package?
There are two alternate ways to fo this, either you can edit the LAMMPS input file to add the extra 'stuffs' corresponsing to the *package* command, or invoke it through command-line keeping the input files unchanged.

If the `package` command is specified in an input script, it must be near the top of the script, before the simulation box has been defined. This is because it specifies settings that the accelerator packages use in their initialization, before a simulation is defined. This command can be used in LAMMPS in two different ways:

* Edit the input file and introduce the line comprising the *package* command in it. This is perfectly fine, but always remember to use this near the top of the script, before the simulation box has been defined. This is because it specifies settings that the accelerator packages use in their initialization, before a simulation is defined. An example of calling the *GPU package* in a LAMMPS input file is given below:

```
package         gpu 2 neigh yes newton off split 1.0
```
{: .bash}

Additionally, you also need to append an extra "/gpu" suffix wherever applicable. For example, a
pair potential with GPU optimization should be mentioned in the input file as:

```
pair_style      lj/cut/gpu 2.5
```
{: .bash}

* A simpler way to do this is through the command-line when launching LAMMPS using the `-pk`
  command-line switch. The syntax would be exactly the same as when used in an input script:

```
{{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 2 neigh yes newton off split 1.0
```
{: .bash}

The second method appears to be convenient since you don't need to take the hassle to edit the
input file (and possibly in many places)!

Note that there is an extra command-line switch in the above command-line. Do you know what this
is for? To distinguish the various styles of these accelerator packages from its 'regular'
non-accelerated variants, LAMMPS has introduces suffixes and the `-sf` switch  auto-appends these
accelerator suffixes to various styles in the input script. Therefore, when an accelerator package
is invoked through the `-pk` switch (for example, `-pk gpu`), the `-sf` switch ensures that the
appropriate style is also being invoked in the simulation (for example, it ensures that the
`lj/cut/gpu` is used instead of `lj/cut` as `pair_style`).  

In this tutorial, we'll stick to the second method of invoking the accelerator package, i.e.
through the command-line.

> ## Hands-on for the GPU package
>
> Let us start with first example. Below is given a LAMMPS input script for a LJ system. Prepare
> a submission script to run a LAMMPS job with the following input file using 2 gpus. For this run,
> make sure that the neighbour list is built on the CPUs, and a dynamic load-balancing between the
> CPUs and GPUs.
>
> ```
> {% include /snippets/ep05/in.lj %}
> ```
> {: .input}
>
> > ## Solution
> >
> > (FIX ME)
> {: .solution}
{: .challenge}

## Know about the GPU package output

At this stage, once you complete a job successfully, it is time to look for a few things in the
LAMMPS output file. A few of them are for the sanity check to see if LAMMPS is doing the things
that you asked for and a few of them tell you about the performances.

## Device information

It prints about the device information both in the screen-output and the log file. You would notice
something like this:

```
{% include /snippets/ep05/lammps-gpu-output-1.txt %}
```
{: .output}

The first thing that you should notice here is that it's using an *acceleration* for the pair potential lj/cut
and fir this purpose it is using two devices (Device 0 and Device 1) and 12 MPI-processes per
device. That is what you asked for: 2 GPUs (```-pk gpu 2```) and 
`{{ site.sched_comment }} {{ site.sched_flag_ntasks }}=24`. Number of tasks is shared equally by
each GPU. The detail about the graphics card is also printed, *Tesla K80, 13 CU, etc. etc.* along
with the *numerical precision* of the implemented *GPU package* is also printed. In this case, it
is using *double precision*. Next it shows how the MPI-processes are spawned with a GPU core.

## Accelerated version of pair-potential

This section of the output shows you that it is actually using the *accelerated* version of the
pair potential *lj/cut*. You can see that it is using *lj/cut/gpu* though in your input file you
mentioned this as *pair_style  lj/cut 2.5*. This is what happens when you use the *-sf gpu*
command-line switch. This automatically ensures that the correct accelerated version is called for
this run.
```
{% include /snippets/ep05/lammps-gpu-output-2.txt %}
```
{: .output}
 
## Performance section

The following screen-output tells you all about the performance. Some of these terms are already
discussed in previous episode (episode 4). When you the *GPU package* you would see an extra block
of information known as *Device Time Info (average)*. This gives you a total breakdown saying how
the devices (GPUs) have been utilised to do various parts of the job.

``` 
{% include /snippets/ep05/lammps-gpu-output-3.txt %}
```
{: .output}

You should now know how to submit a LAMMPS job that uses GPU package as an accelerator. This is
quite simple, though optimizing the run may not be that straight-forward. You can have numerous
possibilities of choosing the *argument* and the *keywords*. Not only that, the host CPU might have
 multiple cores. More choices would arise from here. 

By rule of thumb, you must have at least same number of MPI processes as the number of GPU cores
available to you. But often, using many MPI tasks per GPU gives you the best performance. As an
example, if you have 4 physical GPUs, you must initiate 4 MPI processes for this job. But, assume
that you have a CPU with 12 cores. This gives you flexibility to use at most 12 MPI processes and
the possible combinations are 4gpu/4cpu, 4gpu/8cpu and 4gpu/12cpu. Though it may sound like that
4gpu/12cpu will provide the maximum speed-up, that may not be the case! This entirely depends on
the problem and also on other settings which can in general be controlled by the *keywords*
mentioned in the above table. Moreover, one may find that for a particular problem using 2 GPUs in
stead of 4 GPUs may give better performance, and this why this is advisable to figure out the best
possible set of run-time parameters following a thorough optimization before  starting the
production runs. This might save your lot of resource and time!

> ## Challenge 2
> 
> **(FIXME) Might not be generic enough** Assume that you have an access to a computing node having
> 4 GPUs and 24 CPU cores. You are also told that you need to find out whether building neighbour
> list on CPU or GPU is more beneficial. You should also look for which is best strategy for the
> force-calculations i.e. offloading the force-calculation job entirely to the GPUs or to find a
> balance between CPUs and GPUs.  This means that you need to submit several runs with various
> settings involving number of MPI tasks, number of GPUs, and relevant command-line switches. So
> many possibilities exist! Can you show 10 (**FIXME 4-5 maybe enough?**) different command-line
> options that you might like to use for your run?
>
>> ## Solution
>>
>> 1. 2GPU/1 MPI task per GPU, Neighbour list building on GPU, force-calculation entirely on GPU
>>
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} = 2 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 2 neigh yes newton off split 1.0
>> ```
>> {: .bash}
>>
>> 2. 2 GPUs/12 MPI proc per GPU, Neighbour list building on CPUs, force-calculation optimum load-balancing
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} = 24 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 4 neigh yes newton off split -1.0 
>> ```
>> {: .bash}
>>
>> 3. (FIXME below!) **Do we really need 10?? Surely 3 or 4 is enough!)
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} =4 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 4 neigh yes newton off split 1.0
>> ```
>> {: .bash}
>>
>> 4. 
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} =4 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 4 neigh yes newton off split 1.0
>> ```
>> {: .bash}
>>
>> 5.
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} =4 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 4 neigh yes newton off split 1.0
>> ```
>> {: .bash}
>>
>> 6. 
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} =4 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 4 neigh yes newton off split 1.0
>> ```
>> {: .bash}
>>
>> 7. 
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} =4 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 4 neigh yes newton off split 1.0
>> ```
>> {: .bash}
>>
>> 8. 
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} =4 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 4 neigh yes newton off split 1.0
>> ```
>> {: .bash}
>>
>> 9. 
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} =4 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 4 neigh yes newton off split 1.0
>> ```
>> {: .bash}
>>
>> 10. 
>> ```
>> {{ site.sched_comment }} {{ site.sched_flag_ntasks }} =4 
>> {{ site.run_openmp }} {{ site.sched_lammps_exec }} -in in.lj -sf gpu -pk gpu 4 neigh yes newton off split 1.0
>> ```
>> {: .bash}
>>
> {: .solution}
{: .challenge}

> ## Challenge 3: Optimization
> 
> Use the above input file and submit as many jobs as required to optimize the run-time parameters
> for the best performance from 1 node.
>
>> ## Solution
>>
>> 1. Make a plot of walltime (in sec) vs #gpu/#cpu for ```neigh yes newton off split -1.0```
>> 2. Do the same for ```neigh yes newton off split 1.0```
>> 3. Repeat it again for ```neigh no newton off split -1.0``` and ```neigh no newton off split 1.0```
>> 4. Make 4 different plots and comment on which one is the best performing settings.
> {: .solution}
{: .challenge}

> ## Kokkos package
>
> (**FIX ME!**)
{: .callout}

{% include links.md %}
