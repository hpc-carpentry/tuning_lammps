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
 

> ## Before you start
> 
> 1. **Know your host:** get the number of physical cores per node available to you. 
> 2. **Know your device:** Fix Me
> 3. **Check for hyperthreading:** Sometimes a CPU splits its each physical cores into multiple virtual cores known as threads. In Intel's term, this is called hyperthreads (HT). When hyperthreading is enabled, each physical core appears as two logical CPU units to the OS and thus allows these logical cores to share the physical execution space. This may result in a 'slight' performance gain.  (FIX ME)
> 3. **Fix CPU affinity:** --bind-to core
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
> > ... ... ...
> > ... ... ...
> > srun lmp -k on g 4 -sf kk -pk kokkos -in in.lj
> > ~~~
> > {: .input}
> {: .solution}
{: .challenge}

> ## A few tips on availing speedup from Kokkos/GPU (collected from [LAMMPS website](https://lammps.sandia.gov/doc/Speed_kokkos.html))
> 
> 1. **Hardware comptibility**: For better performance, you must use *Kepler* or later generations of GPUs.
> 2. **MPI tasks per GPU**: You should use one MPI task per GPU because Kokkos tries to run everything on the GPU, including the integrator and other fixes/computes. One may get better performance by assigning multiple MPI tasks per GPU if some styles used in the input script have not yet been Kokkos-enabled.
> 3. **CUDA-aware MPI library**: Using this can provide significant performance gain wherever possible. If this is not available, set it *off* using the `-pk kokkos cuda/aware no` switch.
> 4. **neigh and newton**: For Kokkos/GPU, the default is *neigh = full* and *newton = off*. For *Maxwell* and *Kepler* generations of GPUs, the *default* settings are typically the best. For *Pascal* generations, setting *neigh = half* and *newton = on* might produce faster runs.
> 5. **binsize**: For many pair styles, setting the value of *binsize* to twice that used for the CPU styles could offer speedup (and this is the *default* for the Kokkos/GPU style)
> 6. **Avoid mixing Kokkos and non-Kokkos styles**: In the LAMMPS input file, if you use styles that are not ported to use Kokkos, you may experience a significant loss in performance. This performance penalty occurs because it causes the data to be copied back to the CPU repeatedly. 
{: .callout}

In the following discussion, we'll work on a few exercises to get familiarized on some of these aspects to some extent.

## Exercise 1: performance penalty due to use of mixed styles
  1. First, let us take the input for the LJ-system from the Exercise 1 of the GPU section in Episode 5 (Let us call this as *Input 1*). Run this input using all the visible devices in a node available to you and use Kokkos/GPU as the accelerator package using the following setting: `-k on g 4 -sf kk -pk kokkos newton off neigh full comm device cuda/aware off`. Use the number of MPI tasks that equals to the number of devices.
  2. Measure the performance of this run in units of *timesteps/s*. 
  3. Now, modify the above LJ-input file as shown below. In this case, we'll append a few extra lines near the end of the file. Let us name this modified input file as *Input 2*. Run this input using the same identical Kokkos setting: `-k on g 4 -sf kk -pk kokkos newton off neigh full comm device cuda/aware off`, and with identical number of GPU and MPI tasks as you did for the task 1.
  4. Again, measure the performance of this run in units of *timesteps/s*. 
  5. Compare between the performance of these two runs and comment on your observations.
  
  ```
  ... ... ...
  ... ... ...
  neighbor	0.3 bin
  neigh_modify	delay 0 every 20 check no
  
  compute 1 all coord/atom cutoff 2.5
  compute 2 all reduce sum c_1
  variable acn equal c_2/atoms
  
  fix		1 all nve
  
  thermo 50
  thermo_style custom step time  temp press pe ke etotal density v_acn
  run		500
  ```
 

### Solution
I did this study in a Intel Xeon E5-2680 v3 Haswell CPU node having 2x12 cores per node and two NVIDIA K80 GPUs (four visible devices per node: 2 x 4992 CUDA cores, 2 x 24 GiB GDDR5 memory) with Mellanox EDR InfiniBand high-speed network with non-blocking fat tree topology. I have  used 1 MPI tasks per GPU. This means that for four visible devices we have used four MPI tasks in total.  
First, we ran with the input file as provided in the exercise 1 of the GPU section in episode 5. Second, we modified this input as mentioned above and performance for both of these runs are measured in units of *timesteps/s*. We can get this information from the log/screen output files. The comparison of performance is given in this table:

|Input | Performance (timesteps/sec) |  Performance lost by a factor of |
|------|-----------------------------|----------------------------------|
|Input 1 (all Kokkos enabled styles used)| 8.097                   |                                 |
|Input 2 (non-Kokkos style used: *compute coord/atom*) | 3.022        |  2.68                           |

In *Input 2* we have used styles that is not yet ported to Kokkos. We can check this from the log/screen output files:
> ~~~
>  (1) pair lj/cut/kk, perpetual
>      attributes: full, newton off, kokkos_device
>     pair build: full/bin/kk/device
>      stencil: full/bin/3d
>      bin: kk/device
> (2) compute coord/atom, occasional
>      attributes: full, newton off
>      pair build: full/bin/atomonly
>      stencil: full/bin/3d
>     bin: standard
> ~~~
{: .output}
In this case, the pair style is Kokkos-enabled (`pair lj/cut/kk`) while the compute style `compute coord/atom` is not. Whenever you make such a mix of Kokkos and non-Kokkos styles in the input of a Kokkos run, it costs you dearly since this requires the data to be copied back to the host incurring performance penalty. 


## Exercise ?: Speed-up ( CPU versus GPU package versus Kokkos/GPU )
We have already discussed that the primary aim of developing the Kokkos package is to write a single C++ code that will run on both devices (like GPU, KNL) and hosts (CPU) with or without multi-threading. Targeting portability without losing the functionality and the performance of a code is the primary objective of Kokkos. 
Let us see now see how the current Kokkos/GPU implementation within LAMMPS (version 3Mar20) achieves this goal by comparing its performance with the CPU and GPU package. For this, we shall repeat the same set of tasks as described in exercise 4 of episode 5, GPU section. Take a LJ-system with ~11 million atons by choosing *x* = *y* = *z* = 140 and *t* = 500. We'll use optimum number of GPU devices and MPI tasks to run the jobs with Kokkos/GPU with several number of node counts. Kokkos/GPU is also specially designed to run everything on the GPUs. We shall offload the entire force computation and neighbour list building to the GPUs. This can be done using `-k on g 4 -sf kk -pk kokkos newton off neigh full comm device cuda/aware on` or `-k on g 4 -sf kk -pk kokkos newton off neigh full comm device cuda/aware off` (if *CUDA-aware MPI* is not available to you).

* Do a systamatic study by running the job with different number of nodes with the Kokkos/GPU package. For example, if five nodes are available to you, run this job using all the physical cores available with 1 node, 2 nodes, 3 nodes, 4 nodes and 5 nodes. 
  * Extract the performance data from the log/screen output files from each of these runs. You can do this using the command `grep "Performance:" log.lammps` and note down the performance value in units if *timestep/s*. 
  * Make a plot to comapare the performance of the Kokkos/GPU runs with the CPU runs (i.e. without any accelerator package) and the GPU runs (i.e. with the GPU package enabled) with number of nodes. 
  * Plot the speed-up factor (= GPU performance/CPU performance) versus the number of nodes.
  * Discuss the main observations from these plots.

### Solution

![CPUvsGPUvsKKGPU](../fig/08/CPUvsGPUvsKKGPU.png)

{% include links.md %}

