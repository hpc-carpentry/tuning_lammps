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

The input file for the LJ-system is given below: 
>
> ~~~
> {% include /snippets/ep02/in.lj %}
> ~~~
{: .output}

Before prceeding further, though we assume here that you already know how to run a LAMMPS job in a HPC, let us have a quick recap on how to submit a LAMMPS job in a HPC and understand the output files.


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
