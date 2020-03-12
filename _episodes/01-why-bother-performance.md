---
title: "Why bother with performance?"
teaching: 10
exercises: 5
questions:
- "Why is software performance important?"
- "How can performance be measured?"
- "What is meant by flops, walltime and cpuh?"
- "What affects performance?"
objectives:
- "Understand the necessity of code optimisation"
- "Identify the different methods of enhancing performance"
- "Calculate walltime, cpuh"
keypoints:
- "Understanding performance is the best way of utilising your HPC resources"
- "(FIXME)"
---

## What is software performance?

(FIXME)

## Why is software performance important?

(FIXME)

> ## Enchancing performance: rationale
>
> How long will the example below take to run on one core?
> ```
> 
> ```
> {: language-bash}
> 
>> ## Solution
>> This equates to a whole lifetime. As no-one is going to wait that long for a calculation to run, it provides the motivation we need to speed up the code we have in the best possible way.
>>
>{: .solution}
{: .challenge}

## How is performance measured?

(FIXME)

### Flop

(FIXME)

### Walltime

(FIXME)

### CPUH

(FIXME)

> ## Calculate CPU hours
> 
> In the following example, calculate the CPU hours required to run the following job. Each node has 40 cores
> 
> ```
> #SBATCH --nodes = 2 
> ```
> {: .bash}
> 
> > ## Solution
> >
> > Walltime xxx hours. CPU hours
> > 
>{: .solution}
{: .challenge}

## How can performance be enhanced?

(FIXME) Mention pool of workers, tuning, OpenMP, MPI, GPU and libraries and will refer to them later

## HPC layout and partitioning

> ## Enhancing Performance
>
> Which of these is a viable way of enhancing performance?
> 1. Utilising more cores
> 2. Utilising more nodes
> 3. Increasing the project walltime and CPUh
> 4. Optimising the code
> 5. Utilising MPI (Message Passing Interface)
> 6. Utilising OpenMP
> 7. Using performance enhancing libraries
> 8. Use GPUs instead of CPUs
> 9. 
> 
> > ## Solution
> > 1. Yes
> > 2. Yes
> > 3. No, increasing walltime and CPUh only increases the duration the code will run for. It does not improve the code performance
> > 4. Yes
> > 5. Yes
> > 6. Yes
> > 7. Yes
> > 8. Yes
> > 9. Yes
> >
>{: .solution}
{: .challenge}

{% include links.md %}
