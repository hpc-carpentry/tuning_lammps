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
{: .input}


The timing information for this run with both 1 and 4 processors is also provided with LAMMPS distribution. So, to benchmark it would be wise to run the same job with same processor settings. Let us now create a batch file to submit this job. 

(Chris - files/01/file_to_include L54)
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
