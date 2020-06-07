---
title: "KOKKOS with GPUs"
teaching: 0
exercises: 0
questions:
- "How do I use KOKKOS on a GPU?"
objectives:
- "Utilise KOKKOS on a specific GPU"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---

## Using GPU acceleration through the Kokkos package

In this episode, we shall learn to how to use GPU acceleration using the Kokkos package in LAMMPS. In episode 5, we have learnt the basic syntax of the `package` command that is used to invoke the *kokkos* package in a LAMMPS run. The main arguments and the corresponding keywords were discussed briefly in that chapter. In this episode, we shall do practical exercises to get hands-on experiences on using those commands. But before proceeding further, once again the key sysntax for calling the GPU acceleration through the *Kokkos* package is given below. 

```
srun lmp -in in.lj -k on g {ngpu} -sf kk -pk kokkos {keywords} {values}
```

## Command-line options to submit a Kokkos GPU job in LAMMPS
To run the Kokkos package, the following three command-line switches are very important:
  1. ```-k on``` : This enables Kokkos at runtime
  2. ```-sf kk``` : This appends the "/kk" suffix to Kokkos-supported LAMMPS styles
  3. ```-pk kokkos``` : This is used to modify the default package kokkos options
  To invoke the GPU with Kokkos, we need an additional command-line switch just following the ```-k on``` switch as shown below:
  4. ```-k on g {ngpu}```: Using this switch you can specify the number of GPU devices that you want to use per node. You also need to request to reserve the GPU devices using `#SBATCH --gres=gpu:{ngpu}` (for *SLURM* users). Replace *ngpu* with an integer value equals to the number of devices that you like to use.
 

> ## Rules for performance
> 
> 1. **Know your host:** get the number of physical cores per node available to you. 
> 2. **Know your device:** Fix Me
> 3. **Check for hyperthreading:** Sometimes a CPU splits its each physical cores into multiple virtual cores known as threads. In Intel's term, this is called hyperthreads (HT). When hyperthreading is enabled, each physical core appears as two logical CPU units to the OS and thus allows these logical cores to share the physical execution space. This may result in a 'slight' performance gain.  (FIX ME)
> 3. **Fix CPU affinity:** --bind-to socket, --bind-to core
> 4. **CUDA-aware MPI**: Check if you have CUDA-aware MPI. (FIX ME)
{: .callout}

> ## Get the full command-line
>
> Derive a command-line to submit a LAMMPS job for the LJ system that you studied for the GPU package (Exercise 4) in Episode 5 such that it invokes the Kokkos GPU to accelarte the job using 2 nodes having 24 cores each, 4 devices per node. Assign all the MPI ranks available to a node to all the devices. Use  *default* package options.
> > ## Soloution
> > ~~~
> > #SBATCH --nodes=2
> > #SBATCH --ntasks-per-node=24
> > #SBATCH --partition=gpus
> > #SBATCH --gres=gpu:4
> > 
> > srun lmp -k on g 4 -sf kk -pk kokkos -in in.lj
> > ~~~
> > {: .input}
> {: .solution}
{: .challenge}


## Case study 2: for NVIDIA GPU architecture


> ## Exercise 3: for users
> 
{: .challenge}

{% include links.md %}

