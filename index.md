---
layout: lesson
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---

This workshop is specifically aimed at running the [LAMMPS](https://lammps.sandia.gov/) software on a HPC system. You may be running LAMMPS on either a desktop, laptop or already on an HPC system, however ineffective use of LAMMPS can lead to running jobs which could take far too long. Using a HPC system effectively can speed up your LAMMPS runs significantly and vastly improve its performance if given the right information, which we aim to cover in this workshop.

Some questions that you may ask yourself are;

* What is meant by the term 'performance' of a software?
* What is the metric of measuring this performance?
* How do I measure standard performance of a software?
* How slow is LAMMPS running on my HPC relative to its standard performance?
* **If a software performance is not optimal in my system, is there something that can I do to accelerate it?**

If you have asked the any of above questions, then you might be a good candidate for taking this course.

An HPC is a complex computing platform that has several hardware components and we often talk about its central processing units (CPU), primary and secondary memories and various interconnects. The processing units do the calculations, and there are many different types/generations. The most basic CPU has only one core. This means that it can do only one job at a time.

In recent days, we talk about multi-core CPUs and graphical processing units (GPU). Naturally, the muti-core CPUs have many processing units that can work in parallel. Similarly, GPUs have many processing units as well but they work differenty than a CPU. If you look at the infrastructure of a modern HPC, you would find that it is a heterogeneous computing system since its computing workforce consists of several components.  Some of these components are built using multi-core CPUs only, others use GPUs, and others are made up using Xeon-Phi components, and there are many more.

> ## Test
> `{{ site.exec_env_kokkos }}`
> 
> `{{ site.exec_env_gpu }}`
{: .callout}

# Workforces on a HPC
HPC is a complex computing platform that has several hardware components and we often talk about its central processing units (cpu), primary and secondary memories and various interconnects. The processing units are the ones that actually do the calculations and if you study the evaluation of these processing units you would be quite amazed to see how many different types/generations they have. The most basic cpu has only one core. This means that it can do only one work at a time.

In recent days, we talk about multi-core cpus and graphical processing units (gpu). Naturally, the muti-core cpus have many processing units that can work in parallel. Similarly the gpus have many processing units as well but they work differenty than a cpu. If you look at the infrastructure of a modern HPC, you would find that it is a heterogeneous computing system since its computing workforce consists of several components.  Some of these components are built using the multi-core cpus only, some of them use the gpus, and some are made up using the Xeon-Phi components, and there could be many more.

On any machine, with different components, they would work differently and therefore a software's performance will vary depending on what component it is being run on, and how optimized the code is for that platform. There are no such complications on a standard desktop or laptop, running on an HPC is very, very different.  

> ## Note
> 
> - This is the draft HPC Carpentry release. Comments and feedback are welcome.
{: .callout}

> ## Prerequisites
>
> - Command line experience is required to take this course as well as shell scripting.
> - Prior experience working on a HPC cluster. If you are new to a HPC cluster we recommend participants to go through [hpc-intro](https://hpc-carpentry.github.io/hpc-intro/).
> - You should be familiar with working with LAMMPS and understand its input files and be able to run LAMMPS jobs in an HPC cluster.
>
{: .prereq}
