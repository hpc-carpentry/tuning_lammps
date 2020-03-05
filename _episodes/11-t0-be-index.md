---
title: "Why should I take this course?"
teaching: 8
exercises: 7
questions:
- "Why would I be taking this course?"
- "What can I expect from this course?"
objectives:
- "Identify performance bottlenecks of running LAMMPS in a HPC cluster"
- "Be enable to use hardware architecture support at run-time using KOKKOS"
- "Be able to identify appropriate run-time input parameters to achieve LAMMPS performance acceleration"
keypoints:
- "Merely running a software like LAMMPS on a HPC may not provide expected performance boostup"
- "To assess performance bottlenecks this is important to benchmark LAMMPS"
- "Performance acceleration of LAMMPS for a specific HPC hardware can be achieved using its Kokkos package"
---
# Why should I take this course?

>Before you start the class, type a few sentences about why you are here.

At this point, I assume that all of you have some level of experiences of running [LAMMPS](https://lammps.sandia.gov/) software on a HPC system. A HPC enable us to run jobs that would either be impossible or much slower either in a Desktop or a laptop. The phrase 'much slower' in the previous sentence is not much informative. The first question that arises here is:
>   * How slow is running LAMMPS on my HPC than its standard performance?

Again, for a novice even this question is vague in some sense. Actually it gives rise to more questions like:
>   * What is meant by the term 'performance' of a software?
>   * What is the metric of measuring this performance?
>   * How to measure standard performance of a software?

and finally, 
>   * if a software performance is not optimal in my system, is there something that can I do to accelerate it? 

If the above questions bother you, then you might be a good candidate for taking this course.

> ## Let us know about your HPC experiences with LAMMPS
> Before moving further, we'll take this opportunity to know a little more about your HPC story. Please feel free to talk to your neighbour or [rubber duck](https://rubberduckdebugging.com/) about your HPC experience, like
>  * What HPC system do you use?
>  * Do you know what kind of processors does it ?
>  * Did you build LAMMPS on this HPC by yourself, or are you using a global veersion that was installed by a sys-admin of the HPC?
>  * What kind of simulations you do with LAMMPS, e.g. molecular dynamic (MD), or QM/MM, or MC, etc etc.?
>  * How big is your 'system', i.e. how many atoms/molecules are there in your simulation box?
>  * How long these run take on average?
>  * ...and finally, are you happy with the time that it takes to run a single job?

# Workforces on a HPC
HPC is a complex computing platform that has several hardware components and we often talk about its central processing units (cpu), primary and secondary memories and various interconnects. The processing units are the ones that actually do the calculations and if you study the evaluation of these processing units you would be quite amazed to see how many different types/generations they have. The most basic cpu has only one core. This means that it can do only one work at a time.

In recent days, we talk about multi-core cpus and graphical processing units (gpu). Naturally, the muti-core cpus have many processing units that can work in parallel. Similarly the gpus have many processing units as well but they work differenty than a cpu. If you look at the infrastructure of a modern HPC, you would find that it is a heterogeneous computing system since its computing workforce consists of several components.  Some of these components are built using the multi-core cpus only, some of them use the gpus, and some are made up using the Xeon-Phi components, and there could be many more. 

As a real-life example of the above scenario, let me describe various computing components of the HPC that I am using at ICHEC. The most recent HPC implementation at ICHEC is known as [Kay](https://www.ichec.ie/about/infrastructure/kay). Kay has four key components:

| component nanme | processing units | How many of them? | cores/node |
|-----------------|------------------|-------------------|---------|
| cluster | Intel Xeon Gold (Skylake)/2.4 GHz/192 GiB RAM | 336 nodes | 40 |
| High memory | Intel Xeon Gold (Skylake)/2.4 GHz/1 TiB RAM | 6 nodes | 40 |
| Phi | Intel Xeon Phi 7210 (KNL)/ 1.3 GHz/ 192 GiB RAM | 16 nodes | 40 |
| GPU | Skylake + 2X NVIDIA Tesla V100 16GB PCI | 16 nodes | 5120 CUDA cores & 640 Tensor cores |

It is evident that these components would work differently and therefore a software performance will vary depending on what component it is being run, and how optimized the code is for that platform. By now, you might have some realization about how different it is to run a LAMMPS job on a laptop or Desktop from running it on a HPC!

> ## Well, let us know a little more about your HPC processing units now
>Take a minute and write down the computing units that your HPC is providing you. 

> ## Have you ever used GPU or Phi to run LAMMPS?
> * Write a few sentences about which components/processors are you running your LAMMPS jobs?
> * Probably, a more enagaing one: Do you know whether your LAMMPS binary was prepared to run optimally on this components? 

{% include links.md %}



