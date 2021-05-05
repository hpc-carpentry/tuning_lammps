---
title: Discussion
---
## Abstraction Draft

>### Sample Submission Script
>
> Example.
>
>```
>#!/bin/bash -x
>#SBATCH --account=youraccount
>#SBATCH --nodes=1
>#SBATCH --ntasks-per-node=1
>#SBATCH --output=mpi-out.%j
>#SBATCH --error=mpi-err.%j
>#SBATCH --time=00:15:00
>#SBATCH --partition=devel
>```
>{: .language-bash}
{: .challenge}

Submit your job using the following; 

```
[{{ site.host_prompt }} {{ site.sched_submit }} ]
```
{: .language-bash}

{% include links.md %}
