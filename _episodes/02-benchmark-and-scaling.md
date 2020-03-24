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

Bechmarking can be viewed like a sprint athelete. The athelete runs a predetermined distance on a particular surface, and a time is recorded. Based on different conditions, such as how dry or wet the surface is, or what the surface is made of, grass, sand, or track, the times of the sprinter to cover a distance (100m, 200m, 400m etc) will differ. If you had no idea where the sprinter was running, or what the conditions were like, if the sprinter sets a certain time you can cross-correlate it with a certain time associated with certain surfaces. 

Benchmarking in computing works in a similar way, as it is a way of assessing the performance of a program or set of programs. Usually codes can be tested on different computer architectures to see how a code performs. Like our sprinter, the times of benchmarks depends on a number of things, software, hardware or the computer itself and its architecture.

## What factors can affect a benchmark?

(FIXME)

## Case study: Benchmarking

(FIXME)

> ## Benchmarking
> 
> From what you have learned in this session, try a benchmark of `this`.
>
{: .challenge}

## Scaling

Scaling in computation is the effective use of resources. To explain this in more detail, lets head back to our chefs again from the previous episode

Let us assume that they are all bound by secrecy, and are not allowed to reveal to you what their craft is, pastry, meat, fish, soup, etc. You have to find out what their specialities are, what do you do? Do a test run and assign a chef to each course. Having a worker set to each task is all well and good, but there are certain combinations which work and some which do not, you might get away with your starter chef preparing a fish course, or your lamb chef switching to cook beef and vice versa, but you wouldn't put your pastry chef in charge of the main meat dish, you leave that to someone more qualified and better suited to the job. Eventually after a few test meals, you find out the best combination and you apply that to all your future meals.

Scalinf in computing works in a similar way, thankfully not to that level of detail where one specific core is suited to one specific task, but finding the best combination is important and can hugely impact your code's performance. As ever with enhancing performance, you may have the resources, but the effective use of the resources is where the challenge lies. Having each chef cooking their specialised dishes would be good scaling, an effective use of your resources, but poor scaling is having your pastry chef doing the main dish, which is an ineffective use of resources.

Good scaling vs poor scaling. How to choose no. of nodes, preventing waste of resources.

(FIXME)

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