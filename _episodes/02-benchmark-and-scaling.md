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

Benchmarking can be viewed like a sprint athelete. The athelete runs a predetermined distance on a particular surface, and a time is recorded. Based on different conditions, such as how dry or wet the surface is, or what the surface is made of, grass, sand, or track, the times of the sprinter to cover a distance (100m, 200m, 400m etc) will differ. If you had no idea where the sprinter was running, or what the conditions were like, if the sprinter sets a certain time you can cross-correlate it with a certain time associated with certain surfaces. 

Benchmarking in computing works in a similar way, as it is a way of assessing the performance of a program or set of programs. Usually codes can be tested on different computer architectures to see how a code performs. Like our sprinter, the times of benchmarks depends on a number of things, software, hardware or the computer itself and its architecture.

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
> #SBATCH --account=myAccount
> #SBATCH --nodes=2
> #SBATCH --ntasks-per-node=24
> #SBATCH --output=mpi-out.%j
> #SBATCH --error=mpi-err.%j
> #SBATCH --time=00:05:00
> #SBATCH --partition=myQueue
>
> ... ... ...
> ... ... ...
> ~~~
> {: .input}
> 
> > ## Solution
> > ~~~
> > #SBATCH --nodes=1
> > #SBATCH --ntasks-per-node=4
> > ~~~
> > {: .input}
> {: .solution}
{: .challenge}

Okay, the rest part of the batch file should now be used to set the LAMMPS environment variables and finally we need to invoke the LAMMPS executable for the run. In all modern HPCs, package specific environment variables are loaded or unloaded using modules. Module is a piece of code that is load or unloaded into Kernal as required thus eliminating the requirement of system reboot each time you need to extend the functionalities of the Kernel. Here we show an example code on how to use the 'module' command to load LAMMPS in Jureca.

~~~
module use /usr/local/software/jureca/OtherStages
module load Stages/Devel-2019a
module load intel-para/2019a
module load LAMMPS/9Jan2020-cuda
~~~
{: .source}

> ## Module 
>
> In the above example, this is evident that 'LAMMPS/9Jan2020-cuda' is the LAMMPS module that load the LAMMPS specific environment variables. Can you tell now why we loaded other modules like intel-para/2019a?
>
> > ## Solution
> > This is because this module was used to build LAMMPS and during runtime LAMMPS execuatble will look for all these libraries etc. 
> {: .solution}
{: .challenge}

Now we'll invoke LAMMPS executable to do the job. This can be done as following
```
srun lmp < in.lj|tee out.lj
```
{: .source}
In this case, lmp is the name of the LAMMPS executable. But, in your HPC it could named something else.

> ## Slurm script: full view
>
> Just following the exercise above can you create a batch file to submit a LAMMPS job for the above input file (say, in.lj) to 1 core only. You will submit the job to a partition/queue named 'batch'. The job is expected to take not more than 5 minutes, and the 'batch' partition allows you to submit jobs not crossing 72 hours time limit. The name of the LAMMPS executable is lmp. 
>
> > ## Solution
> > ~~~
> > #!/bin/bash -x
> > #SBATCH --account=ecam
> > #SBATCH --nodes=1
> > #SBATCH --ntasks-per-node=1
> > #SBATCH --output=mpi-out.%j
> > #SBATCH --error=mpi-err.%j
> > #SBATCH --time=72:00:00
> > #SBATCH --partition=batch
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
Let us now check what are the new files created after the job is finished. You would notice that in this case two files have been created: log.lammps and out.lj. Among these two, 'out.lj' is mainly to capture the screen output that have been generated during the job execution. The one that is created by LAMMPS is log.lammps. 

Once you open the file you will notice that this file contains most of the important information starting from the LAMMPS version, number of processors used for the runs, processor lay out, thermdynamic steps, as well as the timing information. For the purpose of this tutorial, we would like to concentrate more on the timing breakups.  The keywords that are of interest is listed below:

  * how to get wall-time:  key-word search (loop time)
  * Performance prediction: key-word search (Performance)
  * Compare this data among various HPC platforms (JSC/Kay/LAMMPS-data): Benchmark plot
  * Discuss now what could be the probable reasons for such variation of timing (Discuss a bit about cpuinfo)
  * Discuss about 'CPU use' keyword and discuss the cpu-utilization of the MPI processes

## Scaling

Scaling in computation is the effective use of resources. To explain this in more detail, lets head back to our chefs again from the previous episode

Let us assume that they are all bound by secrecy, and are not allowed to reveal to you what their craft is, pastry, meat, fish, soup, etc. You have to find out what their specialities are, what do you do? Do a test run and assign a chef to each course. Having a worker set to each task is all well and good, but there are certain combinations which work and some which do not, you might get away with your starter chef preparing a fish course, or your lamb chef switching to cook beef and vice versa, but you wouldn't put your pastry chef in charge of the main meat dish, you leave that to someone more qualified and better suited to the job. Eventually after a few test meals, you find out the best combination and you apply that to all your future meals.

Scaling in computing works in a similar way, thankfully not to that level of detail where one specific core is suited to one specific task, but finding the best combination is important and can hugely impact your code's performance. As ever with enhancing performance, you may have the resources, but the effective use of the resources is where the challenge lies. Having each chef cooking their specialised dishes would be good scaling, an effective use of your resources, but poor scaling is having your pastry chef doing the main dish, which is an ineffective use of resources.

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