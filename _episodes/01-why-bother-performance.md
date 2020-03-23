---
title: "Why bother with performance?"
teaching: 10
exercises: 5
questions:
- "What is software performance"
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

## What is software performance?

Before getting into the software side of things, lets take a few steps back. Performance is a generic term that applies to may factors of our lives, from physical to mental and engineering. However with software performance the emphasis isn't always on the most powerful machine, it is how you best utilise the power that you have. Say you are the chef in a restaurant and every dish that you do is perfect. You would be able to produce a set 7 course meal for a table of 3-6 without too much difficulty. If your restaurant is full though, it becomes more difficult, as people would be waiting many hours for their food. However if you had a team of 6 additional chefs with you, assisting as well as communicating with each other, delegating tasks, you have a much higher chance of getting the food out on time and coping with a large workload, likely with each concentrating on doing one course 

It's the same with software performance, if you have one process running doing one thing there is usually never an issue. But if you have one doing several things, it will obviously take much longer. Furthermore if you hade several workers working on several tasks, it will take a fraction of the time. That is the essence of software performance, using the resources you have to their best capabilities.

(Right place?)
Let's consider our chefs again, and assume that they are all bound by secrecy, and are not allowed to reveal to you what their craft is, pastry, meat, fish, soup, etc. You have to find out what their specialities are, what do you do? Do a test run and assign a chef to each course. Having a worker set to each task is all well and good, but there are certain combinations which work and some which do not, you might get away with your starter chef preparing a fish course, or your lamb chef switching to cook beef and vice versa, but you wouldn't put your pastry chef in charge of the main meat dish, you leave that to someone more qualified and better suited to the job. Eventually after a few test meals, you find out the best combination and you apply that to all your future meals.

Computing works in a similar way, thankfully not to that level of detail where one specific core is suited to one specific task, but finding the best combination is important and can hugely impact your code's performance. As ever with enhancing performance, you may have the resources, but the effective use of the resources is where the challenge lies
(Right place?)

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
> Flops stands for floating point operations per second and they are typically used to measure the performance of a computer's processor.
>
> The theoretical peak flops is given by `(CHECKME!!!!!!!!!)` Number of cores * Average frequency * Operations per cycle.
{: .callout}

> ## Calculate Flops
> 
> See how many flops your computer is capable of at maximum efficiency.
>
{: .challenge}

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
>{: .solution}
{: .challenge}

The `--time` variable used in the exercise is the amount of CPU hours requested, which will differ from the actual CPU hours the code spent to run.

> ## Requested CPU vs. Actual CPU
>
> See the following LAMMPS output log file and the submission script file. What is the requested CPU hours and the actual CPU hours?
> ```
> run script
> ```
> {: .bash}
>
> ```
> LAMMPS output 
> ```
> {: .bash}
>
> > 
> > ## Solution
> >
> > 
> >
> >{: .solution}
{: challenge}

## How can performance be enhanced?

(FIXME) Mention pool of workers, tuning, OpenMP, MPI, GPU and libraries and will refer to them later

## HPC layout and partitioning

## Optimisation

> ## Enhancing Performance
>
> Enhancing performance is one of the most important things in computation. Which of these are viable ways of enhancing performance? There may be more than one correct answer.
>
> 1. Utilising more cores and nodes
> 2. Increasing the simulation walltime and CPUh
> 3. Optimising the code
> 4. Having a computer with higher flops
> 
> > ## Solution
> > 1. Yes, the more cores and nodes you have, the more work can be distributed across those cores.
> > 2. No, increasing simulation walltime and CPUh only increases the duration the code will run for. It does not improve the code performance.
> > 3. Yes, making the code more efficient by cutting out unnecessary loops and bottlenecks can greatly increase performance.
> > 4. Yes, the faster the computer, the faster the code can run, however, this may not always be possible logistically.
> >
> > As you can see, there are a lot of right answers, however some methods work better than others, and it can entirely depend on the problem you are trying to solve.
> >
>{: .solution}
{: .challenge}

If these terms are unfamiliar now, don't worry as we will cover them over the duration of this course.

> ## Increasing core count
>
> Say you've actually got a powerful laptop or computer at you disposal though, you want to ideally 
>
> 1. Utilising MPI (Message Passing Interface)
> 2. Utilising OpenMP (Open Multi-Processing)
> 3. Using performance enhancing libraries
> 4. Use GPUs instead of CPUs
> 5. Splitting code up into smaller segments
>
> > 1. Yes, MPI can enable you to split your code into multiple processes distributed over multiple cores, known as parallel programming.
> > 2. Yes, like MPI this is also parallel programming, but deals with threads, by splitting a process into multiple threads, each thread using a single core.
> > 3. Yes, that is their purpose. Different libraries run on different architectures however.
> > 4. Yes, GPUs are better at handling multiple tasks, whereas a CPU is better running singular tasks quickly.
> > 5. No, if you have a simulation that needs to be run from start to completion, splitting the code into segments won't be of any benefit and will waste compute resources.
>{: .solution}
{: .challenge}

{% include links.md %}
