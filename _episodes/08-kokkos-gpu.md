---
title: "Kokkos with GPUs"
teaching: 15
exercises: 15
questions:
- "How do I use Kokkos together with a GPU?"
objectives:
- "Utilise Kokkos on a specific GPU"
keypoints:
- "Knowing the capabilities of your host, device and if you can use a CUDA-aware MPI
  runtime is required before starting a GPU run"
-
---

## Using GPU acceleration through the **Kokkos** package

In this episode, we shall learn to how to use GPU acceleration using the **Kokkos**
package in LAMMPS. In a
[previous episode]({{page.root}}{% link _episodes/06-invoking-kokkos.md %}), we
have learnt the basic syntax of the `package` command that
is used to invoke the **Kokkos** package in a LAMMPS run. The main arguments and the
corresponding keywords were discussed briefly in that chapter. In this episode, we shall
do practical exercises to get further hands-on experiences on using those commands.

## Command-line options to submit a Kokkos GPU job in LAMMPS

In this episode, we'll learn to use **Kokkos** package with GPUs. As we have seen,
to run the **Kokkos** package the following three command-line switches are very important:
  1. ```-k on``` : This enables Kokkos at runtime
  2. ```-sf kk``` : This appends the "/kk" suffix to Kokkos-supported LAMMPS styles
  3. ```-pk kokkos``` : This is used to modify the default package **Kokkos** options

To invoke the GPU execution mode with Kokkos, the ```-k on``` switch takes additional
arguments for hardware settings as shown below:
  4. ```-k on g Ngpu```: Using this switch you can specify the number of GPU devices, `Ngpu`,
     that you want to use per node.


> ## Before you start
>
> 1. **Know your host:** get the number of physical cores per node available to you.
> 2. **Know your device:** know how many GPUs are available on your system and know how
>    to ask for them from your *resource manager* (SLURM, etc.)
> 4. **CUDA-aware MPI**: Check if you can use a CUDA-aware MPI runtime with your LAMMPS
>    executable. If not then you will need to add `cuda/aware no` to your `<arguments>`.
{: .callout}

> ## Creating a Kokkos GPU job script
>
> Create a job script to submit a LAMMPS job for the [LJ system that you studied for the
> **GPU**
> package]({{page.root}}{% link _episodes/05-accelerating-lammps.md %}#learn-to-call-the-gpu-package-from-the-command-line)
> such that it invokes the Kokkos GPU to
> * accelerate the job using 2 nodes,
> * uses all available GPU devices on the node,
> * use the same amount of MPI ranks per node as there are GPUs, and
> * uses the *default* package options.
>
> > ## Solution
> >
> > {% capture mycode %}{% include {{ site.snippets }}/ep08/gpu_kokkos_job_script %}{% endcapture %}
> > {% assign lines_of_code = mycode | strip |newline_to_br | strip_newlines | split: "<br />" %}
> > ~~~{% for member in lines_of_code %}
> > {{ member }}{% endfor %}
> > ~~~
> > {: .language-bash}
> > If you run it how does the execution time compare to the times you have seen for the
> > **GPU** package?
> {: .solution}
{: .challenge}

> ## A few tips on gaining speedup from **Kokkos**/GPU
>
> This information is collected from the
> [LAMMPS website](https://lammps.sandia.gov/doc/Speed_kokkos.html)
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
>    copied back and forth from the CPU repeatedly.
{: .callout}

In the following discussion, we'll work on a few exercises to get familiarized on some of
these aspects (to some extent).

> ## Exercise: Performance penalty due to use of mixed styles
>
> 1. First, let us take the input and job script for the LJ-system in the last exercise.
>    Make a copy of this script that uses the following additional settings:
>    * `newton off`
>    * `neigh full`
>    * `comm device`
>
>    Use the number of MPI tasks that equals to the number of devices. Measure the performance of
>    of this run in `timesteps/s`.
>
> 2. Make a copy of the LJ-input file called `in.mod.lj` and append the following lines to
>    the end of the file:
>
>    ~~~
>    ... ... ...
>    ... ... ...
>    neighbor	0.3 bin
>    neigh_modify	delay 0 every 20 check no
>
>    compute 1 all coord/atom cutoff 2.5
>    compute 2 all reduce sum c_1
>    variable acn equal c_2/atoms
>
>    fix		1 all nve
>
>    thermo 50
>    thermo_style custom step time  temp press pe ke etotal density v_acn
>    run		500
>    ~~~
>    {: .source}
>
> 3. Using the same Kokkos setting as before, and the identical
>    number of GPU and MPI tasks as previously, run the job script using the new input file.
>    Measure the performance of this run in `timesteps/s`
>    and compare the performance of these two runs. Comment on your observations.
>
> > ## Solution
> >
> > Taking an example from a HPC system with 2x12 cores per node and 2 GPUs (4 visible devices per
> > node), using 1 MPI task per GPU, the following was observed.
> >
> > First, we ran with `in.lj`. Second, we modified this input as mentioned above (to
> > become `in.mod.lj`) and performance for both of these runs are measured in units of
> > `timesteps/s`. We can get this information from the log/screen output files. The
> > comparison of performance is given in this table:
> >
> > |Input | Performance (timesteps/sec) |  Performance loss |
> > |------|-----------------------------|----------------------------------|
> > |`in.lj` (all Kokkos enabled styles used)| 8.097                   |                                 |
> > |`in.mod.lj` (non-Kokkos style used: `compute coord/atom`) | 3.022        |  2.68                           |
> >
> > In `in.mod.lj` we have used styles that are not yet ported to Kokkos. We can check this
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
> >
> > In this case, the pair style is Kokkos-enabled (`pair lj/cut/kk`) while the compute
> > style `compute coord/atom` is not. Whenever you make such a mix of Kokkos and
> > non-Kokkos styles in the input of a Kokkos run, it costs you dearly since this
> > requires the data to be copied back to the host incurring a performance penalty.
> {: .solution}
{: .challenge}

We have already discussed that the primary aim of developing the Kokkos package is to write a
single C++ code that will run on both devices (like GPU) and hosts (CPU) with or without
multi-threading. Targeting portability without losing the functionality and the performance of a
code is the primary objective of Kokkos.


> ## Exercise: Speed-up ( CPU versus GPU package versus Kokkos/GPU )
>
> Let us see now see how the current Kokkos/GPU implementation within LAMMPS (version
> `3Mar20`) achieves this goal by comparing its performance with the CPU and GPU package.
>
> For this, we shall repeat the same set of tasks as described in
> [episode 5]({{page.root}}/05-accelerating-lammps). Take a
> LJ-system with ~11 million atons by choosing `x = y = z = 140` and `t = 500`. We'll
> Use the optimum number of GPU devices and MPI tasks to run the jobs with **Kokkos**/GPU
> with 1 node, then **any of** 2, 3, 4, 5 nodes (2 sets: one with
> the **GPU** package enabled, and the other is the regular **MPI-based** runs **without any**
> accelerator package). *For a better comparison of points, choose a different multi-node number*
> *to that of your neighbour*.
>
> **Kokkos**/GPU is also specially designed to run
> everything on the GPUs. We shall offload the entire force computation and neighbour
> list building to the GPUs using;
>
> ```
> -k on g 4 -sf kk -pk kokkos newton off neigh full comm device
> ```
 {: .bash}
> or
> ```
> -k on g 4 -sf kk -pk kokkos newton off neigh full comm device cuda/aware off
> ```
> {: .bash}
>
> (if *CUDA-aware MPI* is not available to you).
>
> * Extract the performance data from the log/screen output files from each of these
>   runs. You can do this using the command
>   ```
>   grep "Performance:" log.lammps
>   ```
>   {: .bash}
>   and note down the performance value in units of `timestep/s`.
>
> * Make a plot to compare the performance of the **Kokkos**/GPU runs with the CPU runs
>   (i.e. without any accelerator package) and the **GPU** runs (i.e. with the **GPU**
>   package enabled) with number of nodes.
>
> * Plot the speed-up factor (= GPU performance/CPU performance) versus the number of
>   nodes.
>
> * Discuss the main observations from these plots.
>
> > ## Solution
> >
> > <p align="center"><img src="../fig/08/CPUvsGPUvsKKGPU.png" width="50%"/></p>
> >
> > **FIXME**
> {: .solution}
{: .challenge}
