---
title: "Kokkos with GPUs"
teaching: 0
exercises: 0
questions:
- "How do I use Kokkos on a GPU?"
objectives:
- "Utilise Kokkos on a specific GPU"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---

## Using GPU acceleration through the **Kokkos** package

In this episode, we shall learn to how to use GPU acceleration using the **Kokkos**
package in LAMMPS. In [a previous episode]({{page.root}}/06-invoking-kokkos), we
have learnt the basic syntax of the `package` command that
is used to invoke the **Kokkos** package in a LAMMPS run. The main arguments and the
corresponding keywords were discussed briefly in that chapter. In this episode, we shall
do practical exercises to get more hands-on experiences on using those commands.

## Command-line options to submit a Kokkos GPU job in LAMMPS

Before proceeding further, let's breakdown the key syntax for calling the GPU acceleration
through the **Kokkos** package is given below.

```
srun lmp -in in.lj -k on g Ngpu -sf kk -pk kokkos <arguments>
```
{: .bash}
To run the **Kokkos** package, the following three command-line switches are very important:
  1. ```-k on``` : This enables Kokkos at runtime
  2. ```-sf kk``` : This appends the "/kk" suffix to Kokkos-supported LAMMPS styles
  3. ```-pk kokkos``` : This is used to modify the default **Kokkos** package options

To invoke the GPU(s) with **Kokkos**, we need an additional command-line switch just following
the ```-k on``` switch as shown below:
  4. ```-k on g Ngpu```: Using this switch you can specify the number of GPU devices, `Ngpu`,
     that you want to use per node.


> ## Before you start
>
> 1. **Know your host:** get the number of physical cores per node available to you.
> 2. **Know your device:** know how many GPUs are available on your system and know how
>    to ask for them from your *resource manager* (SLURM, etc.)
> 4. **CUDA-aware MPI**: Check if you can use a CUDA-aware MPI runtime with your LAMMPS
>    executable. If not then you need to add `cuda/aware no` to your `<arguments>`.
{: .callout}

> ## Get the full command-line
>
> Derive a command-line to submit a LAMMPS job for the LJ system that you studied for
> the GPU package (***ADD REF***) such that it invokes the Kokkos GPU to
> accelerate the job using 2 nodes having 24 cores each, 4 devices per node. Assign all
> the MPI ranks available on a node to all the devices. Use  *default* package options.
> > ## Solution
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

> ## A few tips on gaining speedup from **Kokkos**/GPU
>
> This information is collected from the
> [LAMMPS website](https://lammps.sandia.gov/doc/Speed_kokkos.html))
>
> 1. **Hardware comptibility**: For better performance, you must use *Kepler* or later
>    generations of GPUs.
> 2. **MPI tasks per GPU**: You should use one MPI task per GPU because Kokkos tries to
>    run everything on the GPU, including the integrator and other fixes/computes. One
>    may get better performance by assigning multiple MPI tasks per GPU if some styles
>    used in the input script have not yet been Kokkos-enabled.
> 3. **CUDA-aware MPI library**: Using this can provide significant performance gain.
>    If this is not available, set it `off` using the `-pk kokkos cuda/aware no` switch.
> 4. **`neigh` and `newton`**: For Kokkos/GPU, the default is `neigh = full` and
>    `newton = off`. For *Maxwell* and *Kepler* generations of GPUs, the *default*
>    settings are typically the best. For *Pascal* generations, setting `neigh = half`
>    and `newton = on` might produce faster runs.
> 5. **binsize**: For many pair styles, setting the value of `binsize` to twice that
>    used for the CPU styles could offer speedup (and this is the *default* for the
>    Kokkos/GPU style)
> 6. **Avoid mixing Kokkos and non-Kokkos styles**: In the LAMMPS input file, if you use
>    styles that are not ported to use Kokkos, you may experience a significant loss in
>    performance. This performance penalty occurs because it causes the data to be
>    copied back to the CPU repeatedly.
{: .callout}

In the following discussion, we'll work on a few exercises to get familiarized on some of
these aspects to some extent.

> ## Exercise: Performance penalty due to use of mixed styles
>   1. First, let us take the input for the LJ-system from the Exercise 1 of the GPU
>      section in Episode 5 (***ADD REF***, let us call this as *Input1*). Run this input
>      using all
>      the visible devices in a node available to you and use **Kokkos**/GPU as the
>      accelerator package using the following settings ***THESE ARE SYSTEM SPECIFIC***:
>      `-k on g 4 -sf kk -pk kokkos newton off neigh full comm device cuda/aware off`. Use
>      the number of MPI tasks that equals to the number of devices.
>   2. Measure the performance of this run in units of `timesteps/s`.
>   3. Now, modify the above LJ-input file and append the following lines to the end of
>      the file:
>      ```
>      ... ... ...
>      ... ... ...
>      neighbor	0.3 bin
>      neigh_modify	delay 0 every 20 check no
>
>      compute 1 all coord/atom cutoff 2.5
>      compute 2 all reduce sum c_1
>      variable acn equal c_2/atoms
>
>      fix		1 all nve
>
>      thermo 50
>      thermo_style custom step time  temp press pe ke etotal density v_acn
>      run		500
>      ```
>      Let us name this modified input file as
>      *Input2*. Run *Input2* using the same identical Kokkos setting:
>      `-k on g 4 -sf kk -pk kokkos newton off neigh full comm device cuda/aware off`
>      and with identical number of GPU and MPI tasks as you did for the *Input1*.
>   4. Again, measure the performance of this run in units of `timesteps/s`.
>   5. Compare the performance between these two runs and comment on your observations.
>
> > ## Solution
> > I did this study in a Intel Haswell CPU node having 2x12 cores per
> > node and two NVIDIA K80 GPUs (which is four visible devices per node). I have used
> > 1 MPI tasks per GPU. This means that for four visible devices we have used four MPI
> > tasks in total (per node).
> >
> > First, we ran with *Input1*. Second, we modified this input as mentioned above (to
> > become *Input2*) and performance for both of these runs are measured in units of
> > `timesteps/s`. We can get this information from the log/screen output files. The
> > comparison of performance is given in this table:
> >
> > |Input | Performance (timesteps/sec) |  Performance loss by a factor of |
> > |------|-----------------------------|----------------------------------|
> > |Input 1 (all Kokkos enabled styles used)| 8.097                   |                                 |
> > |Input 2 (non-Kokkos style used: `compute coord/atom`) | 3.022        |  2.68                           |
> >
> > In *Input2* we have used styles that is not yet ported to Kokkos. We can check this
> > from the log/screen output files:
> > ~~~
> > (1) pair lj/cut/kk, perpetual
> >     attributes: full, newton off, kokkos_device
> >     pair build: full/bin/kk/device
> >     stencil: full/bin/3d
> >     bin: kk/device
> > (2) compute coord/atom, occasional
> >     attributes: full, newton off
> >     pair build: full/bin/atomonly
> >     stencil: full/bin/3d
> >     bin: standard
> > ~~~
> > {: .output}
> > In this case, the pair style is Kokkos-enabled (`pair lj/cut/kk`) while the compute
> > style `compute coord/atom` is not. Whenever you make such a mix of Kokkos and
> > non-Kokkos styles in the input of a Kokkos run, it costs you dearly since this
> > requires the data to be copied back to the host incurring performance penalty.
> {: .solution}
{: .challenge}

> ## Exercise: Speed-up ( CPU versus GPU package versus Kokkos/GPU )
> We have already discussed that the primary aim of developing the Kokkos package is to
> write a single C++ code that will run on both devices (like GPU) and hosts (CPU) with
> or without multi-threading. Targeting portability without losing the functionality and
> the performance of a code is the primary objective of Kokkos.
>
> Let us see now see how the current Kokkos/GPU implementation within LAMMPS (version
> `3Mar20`) achieves this goal by comparing its performance with the CPU and GPU package.
> For this, we shall repeat the same set of tasks as described in ***ADD REF***. Take a
> LJ-system with ~11 million atons by choosing `x = y = z = 140` and `t = 500`. We'll
> use optimum number of GPU devices and MPI tasks to run the jobs with **Kokkos**/GPU
> with several number of node counts. **Kokkos**/GPU is also specially designed to run
> everything on the GPUs. We shall offload the entire force computation and neighbour
> list building to the GPUs. This can be done using
> ```
> -k on g 4 -sf kk -pk kokkos newton off neigh full comm device
> ```
> or
> ```
> -k on g 4 -sf kk -pk kokkos newton off neigh full comm device cuda/aware off
> ```
> (if *CUDA-aware MPI* is not available to you).
>
> * Do a systematic study by running the job with different number of nodes with the
>   Kokkos/GPU package. For example, if five nodes are available to you, run this job
>   using all the physical cores available with 1 node, 2 nodes, 3 nodes, 4 nodes and
>   5 nodes.
> * Extract the performance data from the log/screen output files from each of these
>   runs. You can do this using the command
>   ```
>   grep "Performance:" log.lammps
>   ```
>   {: .bash}
>   and note down the performance value in units if `timestep/s`.
> * Make a plot to compare the performance of the **Kokkos**/GPU runs with the CPU runs
>   (i.e. without any accelerator package) and the **GPU** runs (i.e. with the **GPU**
>   package enabled) with number of nodes.
> * Plot the speed-up factor (= GPU performance/CPU performance) versus the number of
>   nodes.
> * Discuss the main observations from these plots.
>
> > ## Solution
> >
> > <p align="center"><img src="../fig/08/CPUvsGPUvsKKGPU.png" width="50%"/></p>
> {: .solution}
{: .challenge}

{% include links.md %}

