---
layout: reference
permalink: /reference/
root: ..
---

## Glossary

{:auto_ids}
package-OPT
:   As of *3Mar20* version of LAMMPS, the following list of functionalities are available with the OPT package

    | pair styles       |
    | :---------------: |
    |eam_alloy          |
    |eam_fs             |
    |eam                |
    |lj_charmm_coul_long|
    |lj_cut_coul_long   |
    |lj_cut             |
    |lj_cut_tip4p_long  |
    |lj_long_coul_long  |
    |morse              |
    |ufm                |

package-USER-INTEL
:   As of *3Mar20* version of LAMMPS, the following list of functionalities are available with the USER-INTEL package

    | Pair styles         | Bond styles | Angle styles | Improper styles | Dihedral styles | Fix styles | K-space styles | Integrator styles |
    | :-----------------: | :---------: | :----------: | :-------------: | :-------------: | :--------: | :------------: | :---------------: |
    |airebo               | fene        | charmm       | cvff            | charmm          | nve        | pppm           | verlet_lrt        |
    |airebo_morse         | harmonic    | harmonic     | harmonic        | fourier         | nvt        | pppm_disp      |                   |
    |buck_coul_cut        |             |              |                 | harmonic        | npt        |                |                   |
    |buck_coul_long       |             |              |                 | opls            | nh         |                |                   | 
    |buck                 |             |              |                 |                 | nve_asphere|                |                   |
    |dpd                  |             |              |                 |                 | nvt_sllod  |                |                   |
    |eam_alloy            |             |              |                 |                 |            |                |                   |
    |eam_fs               |             |              |                 |                 |            |                |                   |
    |eam                  |             |              |                 |                 |            |                |                   |
    |gayberne             |             |              |                 |                 |            |                |                   |
    |lj_charmm_coul_charmm|             |              |                 |                 |            |                |                   |
    |lj_charmm_coul_long  |             |              |                 |                 |            |                |                   |
    |lj_cut_coul_long     |             |              |                 |                 |            |                |                   |
    |lj_cut               |             |              |                 |                 |            |                |                   |
    |lj_long_coul_long    |             |              |                 |                 |            |                |                   |
    |rebo                 |             |              |                 |                 |            |                |                   |
    |sw                   |             |              |                 |                 |            |                |                   |
    |tersoff              |             |              |                 |                 |            |                |                   |

package-USER-OMP
:   As of *3Mar20* version of LAMMPS, the following list of functionalities are available with the USER-OMP package

package-GPU
:   As of *3Mar20* version of LAMMPS, the following list of functionalities are available with the GPU package

{% include links.md %}
