---
title: "Invoking Kokkos"
teaching: 25
exercises: 5
questions:
- "Why should I use Kokkos?"
- "How do I invoke Kokkos within LAMMPS?"
objectives:
- "Learn how to invoke Kokkos in a LAMMPS run"
- "Learn how to transition from a normal LAMMPS call to an accelerated call"
keypoints:
- "Kokkos is a templated C++ library which allows a *single implementation* of a software application
  on different kinds of hardware"
---
## Kokkos

In recent times, the HPC industry has witnessed dramatic architectural revolution. Modern
HPC architecture
not only includes the conventional multi-core CPUs, but also many-core systems (GPUs are
a good example of this but there are other technologies),
and we don't know yet where this revolution will end up! With the availability of so many
cores for computing,
one would naturally expect a 'scalable' speedup in performance. However, this
scalability does not come
without a cost: it may require several man-years to modify an existing code to make it
compatible with (and efficient on) new hardware architectures.

Why do we need to modify a code for new architectures? This is because innovative
hardware is usually designed with different/innovative philosophies of parallelization in mind,
and these philosophies continue to develop to enhance performance. We frequently now
need to use novel parallelization approaches other than (or as well as) the classic
MPI-based approach to use the latest hardware. For example, on a shared memory platform
one can use OpenMP (not so new), or, on a mixed CPU+GPU platform, one can use CUDA or
OpenACC to parallelize your
codes. The major issue with all these approaches is the performance
portability which arises due to differences in hardware, and software implementations
for hardware (writing CUDA code for NVIDIA GPUs won't help you with Intel Xeon Phi). So,
the question arises: Is there any way to ease this difficulty?

[Kokkos](https://github.com/kokkos) is one of the programming models that strives to be
an answer to this portability issue. The
primary objective of Kokkos is to maximize the
amount of user code that can be compiled for various devices but obtaining comparable
performance as compared to if the code
was written in a  native language specific to that particular device. How does Kokkos
achieve this goal?

1. It maps a C++ *kernel* to different backend languages (like CUDA and OpenMP for example).
2. It also provides data abstractions to adjust (at compile time) the memory layout of
   data structures like 2D
   and 3D arrays to optimize performance on different hardware (e.g., GPUs prefer an opposite
   data layout to CPUs).

> ## Kokkos: A developing library
>
> Why should we bother to learn about using Kokkos?
>
> The primary reason for Kokkos being used by LAMMPS is that it allows you to write a
> *single* pair style in C++ without (much) understanding of GPU programming, that
> will then work on both GPUs (or Xeon Phi or another supported hardware) and CPUs
> with or without multi-threading.
>
> It cannot (currently) fully reach the performance of the **USER-INTEL** or the **GPU**
> packages
> on *particular* CPUs and GPUs, but adding new code for a pair style, for
> which something similar already exists, is *significantly* less effort with Kokkos
> and requires significantly less programming expertise in vectorization and directive
> based SIMD programming or CPU computing. Also support for a new kind of computing
> hardware will primarily need additional code in the Kokkos library and just a
> small amount of programming setup/management in LAMMPS.
>
{: .discussion}

## What is the **Kokkos** package in LAMMPS?

The **Kokkos** package in LAMMPS is implemented to gain performance without losing
portability. Various pair styles, fixes and atom
styles have been updated in LAMMPS to use the data structures and macros as provided by the
Kokkos C++ library so that when LAMMPS is built with Kokkos features enabled targeting
the hardware available on the HPC resource, it can provide
good performance for that hardware when all the runtime parameters are chosen sensibly. What
are the things that it currently supports?

* It can be run on multi-core CPUs, many-core CPUS, NVIDIA GPUs and  and Intel Phis.
* It provides three modes of execution: Serial (MPI-only for CPUs and Phi), OpenMP (via
  threading for many-core CPUs and Phi), and CUDA (for NVIDIA GPUs)
  * It is currently designed for one-to-one CPU to GPU ratio
* Care has been taken to minimize performance overhead due to CPU-GPU communication.
  This can be achieved by ensuring
  that most of the codes can be run on GPUs once assigned by the CPU and when all the
  jobs are done, it is communicated
  back to CPU, thus minimising the amount of data transfer between CPU and GPU.
* It provides reasonable scalability to many OpenMP threads.
* Currently supports double precision only (as of July 2020, but mixed precision is under
  development).
* It is under heavy development and adoption by LAMMPS, so more features and flexibilities
  are expected in future versions of LAMMPS.

The list of LAMMPS features that is supported by Kokkos (as of July 2020) is given below:

| Atom Styles | Pair Styles  | Fix Styles  | Compute Style | Bond Styles | Angle Styles | Dihedral Styles | Improper Styles | K-space Styles |
|:----------- |:------------ |:----------- |:------------- |:----------- |:------------ |:--------------- |:--------------- |:-------------- |
| Angle       |Buck/coul/cut | Deform      | Temp          | Fene        | Charm        | Charm           | Harmonic        | Pppm           |
| Atomic      |Buck/coul/long| Langevin    |               | Harmonic    | Harmonic     | Opls            |                 |                |
| Bond        |Etc.          | Momentum    |               |             |              |                 |                 |                |
| Charge      |Etc.          | Nph         |               |             |              |                 |                 |                |
| Full        |              | Npt         |               |             |              |                 |                 |                |
| Molecular   |              | Nve         |               |             |              |                 |                 |                |
|             |              | Nvt         |               |             |              |                 |                 |                |
|             |              | Qeq/Relax   |               |             |              |                 |                 |                |
|             |              | Reaxc/bonds |               |             |              |                 |                 |                |
|             |              |Reaxc/species|               |             |              |                 |                 |                |
|             |              | Setforce    |               |             |              |                 |                 |                |
|             |              | Wall/reflect|               |             |              |                 |                 |                |

This list is likely to be subject to significant changes over time as newer versions of Kokkos are released.

## How to invoke **Kokkos** package in a LAMMPS run?

In the [previous episode]({{page.root}}{% link _episodes/05-accelerating-lammps.md %}) you learned how to call
an accelerator package in LAMMPS.
The basic syntax of this command is;

```
package <style> <arguments>
```
{: .source}

where `<arguments>` can potentially include a number of *keywords* and their corresponding
*values*.
In this case, you will need to use `kokkos` as `<style>` with suitable arguments/keywords.

For **Kokkos** these *keyword/values* provides you enhanced flexibility to distribute your
job among CPUs and GPUs in an optimum way. As a quick reference, the following table could
be useful:

> ## Guide to Kokkos *keywords*/*values*
>
> | Keywords |what it does? |Default value |
> |----------|--------------|--------------|
> |`neigh`|This keyword determines how a neighbour list is built. Possible values are `half`, `full`  | `full` for GPUs and `half` for CPUs|
> |`neigh/qeq`|  |  |
> |`neigh/thread`|  |  |
> |`newton`|sets the Newton flags for pairwise and bonded interactions to off or on |`off` for GPU and `on` for CPU |
> |`binsize`|sets the size of bins used to bin atoms in neighbor list builds|`0.0` for CPU. On GPUs, the default is twice the CPU value|
> |`comm`|It determines whether the CPU or GPU performs the packing and unpacking of data when communicating per-atom data between processors. Values could be `no`, `host` or `device`. `no` means pack/unpack will be done in non-Kokkos mode| |
> |`comm/exchange`|This defines 'exchange' communication which happens only when neighbour lists are rebuilt. Values could be `no`, `host` or `device` | |
> |`comm/forward`|This defines forward communication and it occurs at every timestep. Values could be `no`, `host` or `device` | |
> |`comm/reverse`| If the `newton` option is set to `on`, this occurs at every timestep. Values could be `no`, `host` or `device`| |
> |`cuda/aware`|This keyword is used to choose whether CUDA-aware MPI will be used. In cases where CUDA-aware MPI is not available, you must explicitly set it to `off` value otherwise it will result in an error.|`off` |
>
>
> ### Rules of thumb
>
> 1. `neigh`: When you use `full` list, all the neighbors of atom `i` are stored with
>    atom `i`. On the contrary, for a `half` list, the `i`-`j` interaction is stored either
>    with atom `i` or `j` but not both. For the GPU, a value of `full` for `neigh` keyword is
>    often more efficient, and in case of CPU a value of `half` is often faster.
> 2. `newton`: Using this keyword you can turn Newton’s 3rd law `on` or `off` for pairwise
>    and bonded interactions. Turning this `on` means less computation and more
>    communication, and setting it `off` means interactions will be calculated by both
>    processors if these interacting atoms are being handled by these two different
>    processors. This results in more computation and less communication. Definitely for
>    GPUs, less communication is usually the better situation. Therefore, a value of `off`
>    for GPUs is efficient while a value of `on` could be faster for CPUs.
> 3. `binsize`: Default value is given in the above table. But there could be exceptions.
>    For example, if you use a larger cutoff for the pairwise potential than the normal,
>    you need to override the default value of `binsize` with a smaller value.
> 4. `comm`, `comm/exchange`, `comm/forward`, `comm/reverse`: From the table you can already
>    tell what it does. Three possible values are `no`, `host` and `device`. For GPUs,
>    `device` is faster if all the styles used in your calculation are Kokkos-enabled. But,
>    if not, it may results in communication overhead due to CPU-GPU communication.
>    For CPU-only systems, `host` is the fastest. For Xeon Phi and CPU-only systems,
>    `host` and `device` work identically.
> 5. `cuda/aware`: When we use regular MPI, multiple instances of an application is
>    launched and distributed to many nodes in a cluster using the MPI application launcher.
>    This passes pointers to host memory to MPI calls. But, when we want to use CUDA and
>    MPI together, it is often required to send data from the GPU instead of the CPU.
>    CUDA-aware MPI allows the GPU data to pass directly through MPI send/receive calls
>    without first which copying the data from device to host, and thus CUDA-aware MPI
>    helps to eliminate the overhead due to this copying process. However, not all HPC systems
>    have the CUDA-aware MPI available and it results in a `Segmentation Fault` error at
>    runtime. We can avoid this error by setting its value to `off` (i.e. `cuda/aware off`).
>    Whenever a CUDA-aware MPI is available to you, you should not need to use this (the
>    default should be faster).
>
{: .callout}

## Invoking Kokkos through input file or through command-line?

Unlike the *USER-OMP* or the *GPU* package in the
[previous episode]({{page.root}}{% link _episodes/05-accelerating-lammps.md %}) which
supports *either* OpenMP
*or* GPU, the **Kokkos** package supports both OpenMP and GPUs. This adds additional
complexity to the command-line to invoke appropriate execution mode (OpenMP or GPU) when
you decide to use **Kokkos** for your LAMMPS runs. In the following section, we'll touch
on a few general command-line features which are needed to call **Kokkos**. More detailed
OpenMP or GPU specific command-line switches will be discussed in later episodes.

Let us recall the command-line to submit a LAMMPS job that uses USER-OMP as an
accelerator package (see
[here]({{page.root}}{% link _episodes/05-accelerating-lammps.md %}#how-to-invoke-the-user-omp-package)
to refresh your memory).

```{% capture mycode %}{% include {{ site.snippets }}/ep05/job_execution_1nodeMPI.snip %}{% endcapture %}
{{ mycode | strip }} -sf omp -pk omp $OMP_NUM_THREADS neigh no
```
{: .language-bash}

We can perform a straight-forward to edit the above command-line to try to make it
appropriate for a **Kokkos** run. A few points to keep in mind:

  1. To enable **Kokkos** package you need to use a switch `-k on`.
  2. To use **Kokkos** enabled styles (pair styles/fixes etc.), you need one additional
     switch `-sf kk`. This will append the `/kk` suffix to all the styles that
     **Kokkos** supports in LAMMPS. For example, when you use this, the
     `lj/charmm/coul/long` pair style would be read as `lj/charmm/coul/long/kk` at runtime.

With these points in mind, the above command-line could be modified
to start making it ready for Kokkos:

```{% capture mycode %}{% include {{ site.snippets }}/ep05/job_execution_1nodeMPI.snip %}{% endcapture %}
{{ mycode | strip }} -k on -sf kk
```
{: .language-bash}

But, unfortunately, this above command-line is still *incomplete*. We have not yet passed any
information about the `package` `<arguments>` yet. These might include information about
the execution mode (OpenMP or GPU), or the number of OpenMP threads,
or the number of GPUs that we want to use for this run, or any other keywords (and
values). We'll discuss more about them in the following episodes.
