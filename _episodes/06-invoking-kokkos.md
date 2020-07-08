---
title: "Invoking KOKKOS"
teaching: 0
exercises: 0
questions:
- "How do I invoke KOKKOS within LAMMPS?"
objectives:
- "Learn how to transition from a normal LAMMPS call to an accelerated call"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
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
free-of-cost, this may require several man-years to modify an existing code to make it
compatible with (and efficient on) new hardware architectures.

Why do we need to modify a code for new architectures? This is because innovative
hardware is designed with different/innovative philosophies of parallelization in mind,
and these philosophies continue to develop to enhance performance. We frequently now
need to use novel parallelization approaches other than (or as well as) the classic
MPI-based approach to use the latest hardware. For example, on a shared memory platform
one can use OpenMP (not so new), or, on a mixed CPU+GPU platform, one can use CUDA or
OpenACC to parallelize your
codes. The major issue with all these approaches is the performance
portability which arises due to differences in hardware, and software implementations
for hardware (writing CUDA code for NVIDIA GPUs won't help you with Intel Xeon Phi). So,
the question arises: Is there any way to ease this difficulty?

Kokkos strives to be an answer to this portability issue. The primary objective of Kokkos
is to maximize the
amount of user code that can be compiled for various devices but obtaining comparable
performance if the code
was written in a  native language specific to that particular device. How does Kokkos
achieve this goal?

1. It maps a C++ kernel to different backend languages like CUDA, OpenMP, Pthreads.
2. It also provides data abstractions to adjust (at compile time) the memory layout of
   data structures like 2D
   and 3D arrays to optimize performance on different hardware.

> ## Kokkos: A developing library
>
> Why should we bother to learn about using Kokkos?
> > ## Solution
> > The primary reason for Kokkos being developed is that it allows you to write a
> > *single* pair style in C++ without (much) understanding of GPU programming, that
> > will then work on both GPUs (or Xeon Phi) and CPUs with or without multi-threading.
> > It cannot (currently) fully reach the performance of USER-INTEL or the GPU package
> > on *particular* CPUs and GPUs, but adding new code to those for a pair style, for
> > which something similar already exists, is *significantly* less effort with Kokkos
> > and requires significantly less programming expertise in vectorization and directive
> > based SIMD programming or CPU computing. Also support for a new kind of computing
> > hardware will primarily need additional code in the Kokkos library and just a
> > little bit of programming setup/management in LAMMPS."
> {: .solution}
{: .discussion}

## What is KOKKOS package in LAMMPS?

Kokkos package in LAMMPS is implemented to gain performance with portability. Various pair styles, fixes and atom
styles have been updated in LAMMPS to use the data structures and macros as provided by the Kokkos C++ library so
that when LAMMPS is built with Kokkos feature enabled for a particular hardware, it can provide optimal performance
for that hardware when all the runtime parameters are chosen sensibly. What are the things that it supports currently?

* It can be run on multi-core CPUs, manycore CPUS and Intel Phis and NVIDIA GPUs.
* It provides three modes of execution: Serial (MPI-only for CPUs and Phi), OpenMP (via threading for manycore CPUs
  and Phi), and CUDA (for NVIDIA GPUs)
* It provides reasonable scalability to many OpenMP threads.
* This is specifically designed for one-to-one CPU to GPU ratio
* Care has been taken to minimize performance overhead due to cpu-gpu communication. This can be achieved by ensuring
  that most of the codes can be run on GPUs once assigned by the CPU and when all the jobs are done, it is communicated
  back to CPU, thus minimising the amount of data transfer between CPU and GPU.
* supports modern GPUs only (an extensive list of supported hardwares are given in LAMMPS [website]().
* Currently supports double precision only.
* Still in developmental stage, so more features and flexibilities are expected in future versions of LAMMPS.

The list of LAMMPS features that is supported by Kokkos is given below:

| Atom Styles | Pair Styles  | Fix Styles  | Compute Style | Bond Styles | Angle Styles | Dihedral Styles | Improper Styles | K-space Styles |
|:----------- |:------------ |:----------- |:------------- |:----------- |:------------ |:--------------- |:--------------- |:-------------- |
| Angle       |Buck/coul/cut | Deform      | Temp          | Fene        | Charm        | Charm           | Harmonic        | Pppm           |
| Atomic      |Buck/coul/long| Langevin    |               | Harmonic    | Harmonic     | Opls            |                 |                |
| Bond        |Etc           | Momentum    |               |             |              |                 |                 |                |
| Charge      |Etc           | Nph         |               |             |              |                 |                 |                |
| Full        |              | Npt         |               |             |              |                 |                 |                |
| Molecular   |              | Nve         |               |             |              |                 |                 |                |
|             |              | Nvt         |               |             |              |                 |                 |                |
|             |              | Qeq/Relax   |               |             |              |                 |                 |                |
|             |              | Reaxc/bonds |               |             |              |                 |                 |                |
|             |              |Reaxc/species|               |             |              |                 |                 |                |
|             |              | Setforce    |               |             |              |                 |                 |                |
|             |              | Wall/reflect|               |             |              |                 |                 |                |


## How to invoke Kokkos package in a LAMMPS run?
You already know how to call an accelerator package in LAMMPS. It was discussed in the previous chapter. The basic syntax of this command is: `*package style args keyword values*`
Obviously, you need to use *kokkos* as *style* with suitable arguments/keywords.

The next you need to choose proper *keywords* and *value* pairs. These *keyword/values* provides you enhanced flexibility to distribute your job among cpu and gpus in an optimum way. For a quick reference, the following table could be useful:

 | Keywords |what it does? |Default value |
 |----------|--------------|--------------|
 |neigh|This keyword determines how a neighbour list is built. Possible values are *half*, *full*  | *full* for GPUs and *half* for CPUs|
 |neigh/qeq|  |  |
 |neigh/thread|  |  |
 |newton|sets the Newton flags for pairwise and bonded interactions to off or on |*off* for GPU and *on* for CPU |
 |binsize|sets the size of bins used to bin atoms in neighbor list builds|*0.0* for CPU and 2x larger binsize equal to the pairwise+neighbour skin|
 |comm|It determines whether the cpu or gpu performs the packing and unpacking of data  when communicating per-atom data between processors. values could be *no*, *host* or *device*. *no* means pack/unpack will be done in non-kokkos mode| |
 |comm/exchange|This defines 'exchange' communication which happens only when neighbour lists are rebuilt. Values could be *no*, *host* or *device* | |
 |comm/forward|This defines forward communication and it occurs at every timestep. Values could be *no*, *host* or *device* | |
 |comm/reverse| If the *newton* option is set to *on*, this occurs at every timestep. Values could be *no*, *host* or *device*| |
 |cuda/aware|This keyword is used to choose whether CUDA-aware MPI will be used. In cases where CUDA-aware MPI is not available, you must explicitly set it to *off* value otherwise it will result is an error.|off |


## Rules of thumb

1. ***neigh***: When you use *full* list, all the neighbors of atom I are stored with atom *I*. On the contrary, for a *half* list, the I-J interaction is stored either with atom *I* or *J* but not both. For GPU, a value of *full* for *neigh* keyword is often more efficient, and in case of CPU a value of *half* is often faster.
2. ***newton***: Using this keyword you can turn Newton’s 3rd law *on* or *off* for pairwise and bonded interactions.
  Turning this *on* means less computation and more communication, and setting it *off* means interactions will be
  calculated by both processors if these interacting atoms are being handled by these two different processors. This
  results in more computation and less communication. Definitely for GPUs, less communication is often a winsome
  situation. Therefore, a value of *off* for GPUs is efficient while a value of *on* could be faster for CPUs.
3. ***binsize***: Default value is given in the above Table. But there could be exception. For example, if you use
  a larger cutoff for the pairwise potential than the normal, you need to override the default value of *binsize*
  with a smaller value.
4. ***comm*, *comm/exchange*, *comm/forward*, *comm/reverse***: You already know what it does (from the above Table).
  Three possible values are *no*, *host* and *device*. For GPUs, *device* is faster if all the styles used in your
  calculation is Kokkos-enabled. But, if not, it may results in communication overhead due to cpu-gpu communication.
  For CPU-only systems, *host* is the fastest. For Xeon Phi and CPU-only systems, *host* and *device* work identically.
5. ***cuda/aware***: When we use regular MPI, multiple instances of an application is launched and distributed to many
  nodes in a cluster using the MPI application launcher known as *mpirun*. This passes pointers to host memory to MPI
  calls. But, when we want to use CUDA and MPI together, it is often required to send GPU buffers instead of CPU
  buffers. CUDA-aware MPI allows GPU buffers to pass directly through MPI send/receive calls without using
  `cudaMemcpy` which copies data from device to host, and thus CUDA-aware MPI helps to eliminate the overhead due to
  this copying process. But, not all HPC systems have the CUDA-aware MPI available. It results in a *Segmentation*
  *Fault* error at runtime. We can avoid this error by setting its value to *off* (i.e. `cuda/aware off`). But,
  whenever a CUDA-aware MPI is available to you, try to exploit it for a Kokkos/GPU run to get the speedup.


## Invoking Kokkos through input file or through command-line?
From episode 5, we already learnt how to use the *package* command to call an accelerator package in a LAMMPS run. Unlike the *USER-OMP* or the *GPU* package which supports either OpenMP or GPU, the *Kokkos* package supports both OpenMP and GPUs. This adds additional complexities in the command-line to invoke appropriate execution mode (OpenMP or GPU) when you decide to use *kokkos* for your LAMMPS runs. Though you can also invoke them through modifying the LAMMPS input file, but it is more convenient to do this through the command-line. In the following section, we'll touch a few general command-line features which are needed to call *Kokkos*. OpenMP specific or GPU specific command-line switches will be discussed in later episodes when we'll be discussing about them in more detail.

Let us recall the command-line to submit a LAMMPS job that uses USER-OMP as an accelerator package (refer to Episode 5, USER-OMP section).
```
mpirun -np 40 -ppn 10 lmp -sf omp -pk omp 4 -in in.rhodo neigh no
```

This is very much straight-forward to edit the above command-line to make it appropriate for a Kokkos run. A few points to keep in mind:

  1. The total number of MPI ranks is set in the usual way via *mpirun* or *mpiexec* or *srun* command. It has nothing to do with Kokkos.
    * `mpirun -np 40 -ppn 10` allows you to submit the job in 4 nodes each of them having 10 MPI processes.
  2. To enable Kokkos package you need to use a switch `-k on`.
  3. To use Kokkos enabled styles (pair styles/fixes etc.), you need one additional switch `-sf kk`. This will append the "/kk" suffix to all the styles that Kokkos supports in LAMMPS. For example, when you use this, the *lj/charmm/coul/long* pair style would be read as *lj/charmm/coul/long/kk* at runtime.

With these points keeping in mind, the above command-line could be modified as following to make it ready for Kokkos:
```
mpirun -np 40 -ppn 10 lmp -k on -sf kk -in in.rhodo
```
But, this above command-line is still *incomplete*. We have not yet passed any information about the execution mode (OpenMP or GPU), or the number of OpenMP threads, or the number of GPUs that we want to use for this run, or the *package* arguments and keywords (and values) to the LAMMPS executable. We'll discussing about them in the following episodes.


{% include links.md %}
