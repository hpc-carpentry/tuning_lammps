---
title: "Invoking KOKKOS"
teaching: 0
exercises: 0
questions:
- "How do I invoke KOKKOS with LAMMPS?"
objectives:
- "Learn how to transition from a normal LAMMPS call to an accelerated call"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---
## Kokkos
In recent times, the HPC industry has witnessed a dramatic architectural revolution. Modern HPC architecture not only includes the conventional multi-core cpus, but also manycore systems like Xeon Phis or Nvidia GPUs, and we don't know yet where this revolution will end up! With the availability of so many cores for computing, one would naturally expect a 'scalable' speedup in performance. However, this scalability does not come free-of-cost, this may require several man-years to modify an existing code to make it compatible for new hardware architectures. Why do we need to modify a code for new architectures? This is because these different hardwres were designed keeping in mind different philosophies of parallelization and these philosophies keep updating at more finer levels to enhance the performance. Some of the architectures prefer data-paralleliztion, while some of them work better for task-level parallelization. So to access the finer levels of parallisation offered by modern day architectures, we often need to use parallizing approaches other than the old classic MPI-based approach. For example, on a shared memory platform one can use OpenMP, or, on a mixed CPU+GPU platform, one can use CUDA or OpenACC to parallize their codes. The major issue with all these approaches is the performance portability which arises due to complex and varying memory access pattern across devices. So, the question arises: Is there any way to ease this difficulty?  

Kokkos is probably an answer to this portability issue. The primary objective of Kokkos is to maximize the amount of user code that can be compiled for various devices but obtaing comparable performance if the code was written in a  native language specific to that particular device. How does Kokkos achieve this goal? 

1. It maps a C++ kernel to different backend languages like Cuda, OpenMP, Pthreads.
2. It also provides data abstractions to adjust (at compile time) the memory layout of data structures like 2d and 3d arrays to optimize performance on different hardware. 

## What is KOKKOS package in LAMMPS?
 Kokkos package in LAMMPS is implemented to gain performance with portability. Various pair styles, fixes and atom styles have been updated in LAMMPS to use the data structures and macros as provided by the Kokkos C++ library so that when LAMMPS is built with Kokkos feature enabled for a particular hardware, it can provide optimal performance for that hardware when all the runtime parameters are choosen sensibly. What are the things that it supports currently? 

* It can be run on multi-core CPUs, manycore CPUS and Intel Phis and NVIDIA GPUs.
* It provides three modes of execution: Serial (MPI-only for CPUs and Phi), OpenMP (via threading for manycore CPUs and Phi), and CUDA (for NVIDIA GPUs)
* It provides reasonable scalability to many OpenMP threads.
* This is specifically designed for one-to-one CPU to GPU ratio
* Care has been taken to minimize performance overhead due to cpu-gpu communication. This can be achieved by ensuring that most of the codes can be run on GPUs once assigned by the CPU and when all the jobs are done, it is communicated back to CPU, thus minimising the amount of data transfer between CPU and GPU.
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
You already know how to call an accelerator package in LAMMPS. It was discussed in the previous chapter. The basic syntax of this command is: *package style args*
Obviously, you need to use *kokkos* as *style* with suitable arguments/keywords.

srun lmp -in in.lj -k on g 4 -sf kk -pk kokkos newton off neigh full comm device cuda/aware off

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
  1. *neigh*: For GPU, a value of *full* for *neigh* keyword is often more efficient, and in case of CPU a value of *half* is often faster.
  2. *newton*: Using this keyword you can turn Newton’s 3rd law *on* or *off* for pairwise and bonded interactions. Turning this *on* means less computation and more communication, and setting it *off* means interactions will be calculated by both processors if these interacting atoms are being handled by these two different processors. This results in more computation and less communication. Definitely for GPUs, less communication is often a winsome situation. Therefore, a value of *off* for GPUs is efficient while a value of *on* could be faster for CPUs.
  3. *binsize*: Default value is given in the above Table. But there could be exception. For example, if you use a larger cutoff for the pairwise potential than the normal, you need to override the default value of *binsize* with a smaller value.
  4. *comm*, *comm/exchange*, *comm/forward*, *comm/reverse*: You already know what it does (from the above Table). Three possible values are *no*, *host* and *device*. For GPUs, *device* is faster if all the styles used in your calculation is Kokkos-enabled. But, if not, it may results in communication overhead due to cpu-gpu communication. For CPU-only systems, *host* is the fastest. For Xeon Phi and CPU-only systems, *host* and *device* work identically. 
  5. cuda/aware: When we use regular MPI, multiple instances of an application is launched and distributed to many nodes in a cluster using the MPI application launcher known as *mpirun*. This passes pointers to host memory to MPI calls. But, when we want to use CUDA and MPI together, it is often required to send GPU buffers instead of CPU buffers. CUDA-aware MPI allows GPU buffers to pass directly through MPI send/receive calls without using ```cudaMemcpy```which copies data from device to host, and thus CUDA-aware MPI helps to eliminate the overhead for this copying process. But, not all HPC systems have the CUDA-aware MPI available. It results in a *Segmentation Fault* error at runtime. We can avoid this error by setting its value to *off* (i.e. ```cuda/aware off```). But, whenever a CUDA-aware MPI is available to you, try to exploit it for a Kokkos/GPU run to get the speedup. 
  
 


> ## Modifying input and submission script
> 
> Analyse the input file `input.lj` and the submission script `run.sh`
> 
> What additional modifications need to be made to make them run under (FIXME) conditions
>
{: .challenge}

{% include links.md %}

