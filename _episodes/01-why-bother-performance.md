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
- "There are many ways of enhancing performance"
- "Just because a way is correct doesn't always mean it is the best option"
---

## What is performance?



## Why is software performance important?

(FIXME)

> ## Enchancing performance: rationale
>
> Imagine you had a 40 x 40 x 40 box like the one below, divided up into smaller boxes, each measuring 1 x 1 x 1. If you wanted and you wanted to simulate what was happening inside each smaller box for 10 hours each How long will the example below take to run on one core?
>
> include 40x40x40_cube.png url="" max-width="40%" file="/fig/01/40x40x40_cube.png" alt="Figure" caption="40 x 40 x 40 cube"
> 
> {: language-bash}
> 
>> ## Solution
>> 
>> 64000 hours or just over 73 years.
>>
>> This is way longer than anyone could bear! But remember, that is utilising just one core. If you had a machine that could simulate each of those smaller boxes simultaneously and a code that enables each box to effectively interact with each other, the whole job would only take roughly 10-12 hours. So it provides the motivation we need to speed up the code we have and utilise the machine to its best capacity
>>
>{: .solution}
{: .challenge}

## How is performance measured?

There are a number of key terms in computing when it comes to understanding performance and expected duration of tasks. The most important of these are flops, walltime and cpuh

> ### Flops
>
> Flops stands for floating point operations per second and they are typically used to measure the performance of a computer's processor
>
{: .callout}


> ### Walltime
> 
> Walltime is simply the length of time, usually measured in seconds that a program takes to run or to execute its assigned tasks. 
>
> This is specified in a submission script when before your task officially starts running. If the task takes longer than the walltime that is specified, the task gets killed and will not complete.
>
{: .callout}

> ### CPUH
>
> CPU hours is the processor time needed to complete a task, i.e. the amount of computing work done. 
>
>
{: .callout}


> ## Calculate CPU hours
> 
> In the following example, assume that you are utilising all the available core in a node. Calculate the CPU hours requested to run the following job. Each node has 40 cores.
> 
> ```
> #SBATCH --nodes = 2
> #SBATCH --time = 05:00:00
> ```
> {: .bash}
> 
> > ## Solution
> >
> > 400 CPUh.
> >
> > 
> > 
>{: .solution}
{: .challenge}

## How can performance be enhanced?

(FIXME) Mention pool of workers, tuning, OpenMP, MPI, GPU and libraries and will refer to them later

## HPC layout and partitioning

> ## Enhancing Performance
>
> Enhacing performance is one of the most important things in computation. Which of these are viable ways of enhancing performance? There may be more than one correct answer.
>
> 1. Utilising more cores
> 2. Utilising more nodes
> 3. Increasing the simulation walltime and CPUh
> 4. Optimising the code
> 5. Utilising MPI (Message Passing Interface)
> 6. Utilising OpenMP (Open Multi-Processing)
> 7. Using performance enhancing libraries
> 8. Use GPUs instead of CPUs
> 9. Having a computer with higher flops
> 10. Use a lower level coding language
> 11. Splitting code up into smaller segments
> 
> > ## Solution
> > 1. Yes, the more cores you have, the more work can be distributed across those cores.
> > 2. Yes, nodes contain multiple cores, the number of which depends on the node. 
> > 3. No, increasing walltime and CPUh only increases the duration the code will run for. It does not improve the code performance.
> > 4. Yes, making the code more efficient by cutting out unnecessary loops and bottlenecks can greatly increase performance.
> > 5. Yes, MPI can enable you to split your code into multiple processes distributed over multiple cores, known as parallel programming.
> > 6. Yes, like MPI this is also parallel programming, but deals with threads, by splitting a process into multiple threads, each thread using a single core.
> > 7. Yes, that is their purpose. Different libraries run on different architectures however.
> > 8. Yes, GPUs are better at handling multiple tasks, whereas a CPU is better running singular tasks quickly.
> > 9. Yes, the faster the computer, the faster the code can run, however, this may not always be possible logistically.
> > 10. Yes, lower level languages (C, C++) run faster than higher level languages (Python) due to there being less abstraction to the machine to handle.
> > 11. No, if you have a simulation that needs to be run from start to completion, splitting the code into segments won't be of any benefit and will waste compute resources.
> >
> > As you can see, there are a lot of right answers, however some methods work better than others, and it can entirely depend on the problem you are trying to solve.
> >
>{: .solution}
{: .challenge}

If these terms are unfamiliar now, don't worry as we will cover them over the duration of this course.

{% include links.md %}
