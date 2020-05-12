---
layout: reference
permalink: /reference/
root: ..
---

## Glossary

{:auto_ids}
package-OPT
:   As of *3Mar20* version of LAMMPS, the following list of functionalities are available with the OPT package

    | Pair styles       |
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
    | :------------------ | :---------- | :----------- | :-------------- | :-------------- | :--------- | :------------- | :---------------- |
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

    | Pair styles         |                       |                               |                        |                      |                         |
    | :------------------ | :-------------------- | :---------------------------- | :--------------------- | :------------------- | :---------------------- |
    |adp                  |agni                   |airebo_morse                   |airbo                   |beck                  |born_coul_long           |
    |born_coul_msm        |born_coul_wolf         |born                           |brownian                |brownian_poly         |buck_coul_cut            |
    |buck_coul_long       |buck_coul_msm          |buck_long_coul_long            |buck                    |colloid               |comb                     |
    |coul_cut             |coul_cut_soft          |coul_debye                     |coul_diel               |coul_dsf              |coul_long                |
    |coul_long_soft       |coul_msm               |coul_wolf                      |dpd                     |dpd_tstat             |eam_alloy                |
    |eam_cd               |eam_fs                 |eam                            |edip                    |eim                   |gauss_cut                |
    |gauss                |gayberne               |gran_hertz_history             |gran_hooke_history      |gran_hooke            |hbond_dreiding_lj        |
    |hbond_dreiding_morse |lj96_cut               |lj_charmm_coul_charmm_implicit |lj_charmm_coul_charmm   |lj_charmm_coul_long   |lj_charmm_coul_long_soft |
    |lj_charmm_coul_msm   |lj_class2_coul_cut     |lj_class2_coul_long            |lj_class2               |lj_cubic              |lj_cut_coul_cut          |
    |lj_cut_coul_cut_soft |lj_cut_coul_debye      |lj_cut_coul_dsf                |lj_cut_coul_long        |lj_cut_coul_long_soft |lj_cut_coul_msm          |
    |lj_cut_coul_wolf     |lj_cut_dipole_cut      |lj_cut                         |lj_cut_soft             |lj_cut_thole_long     |lj_cut_tip4p_cut         |
    |lj_cut_tip4p_long    |lj_cut_tip4p_long_soft |lj_expand                      |lj_gromacs_coul_gromacs |lj_gromacs            |lj_long_coul_long        |
    |lj_long_tip4p_long   |lj_sdk_coul_long       |lj_sdk_coul_msm                |lj_sdk                  |lj_sf_dipole_sf       |lj_smooth_linear         |
    |lj_smooth_linear     |lj_smooth              |lubricate                      |lubricate_poly          |meam_spline           |morse                    |
    |morse_smooth_linear  |nm_cut_coul_cut        |nm_cut_coul_long               |nm_cut                  |peri_lps              |peri_pmb                 |
    |reaxc                |rebo                   |resquared                      |soft                    |sw                    |table                    |
    |tersoff_mod_c        |tersoff_mod            |tersoff                        |tersoff_table           |tersoff_zbl           |tip4p_cut                |
    |tip4p_long           |tip4p_long_soft        |umf                            |vashishta               |vashishta_table       |yukawa_colloid           |
    |yukawa               |zbl                    |                               |                        |                      |                         |

    | Bond styles        | Angle styles     | Improper styles | Dihedral styles  | Fix styles    | K-space styles   |
    | :----------------- | :--------------- | :-------------- | :--------------- | :------------ | :--------------- | 
    | class2             | charmm           | class2          | charmm           | gravity       | pppm_cg          |
    | fene_expand        | class2           | cossq           | class2           | neigh_history | pppm_disp        |
    | fene               | cosine_delta     | cvff            | cosine_shift_exp | nh_asphere    | pppm_disp_tip4p  |
    | gromos             | cosine           | fourier         | fourier          | nh            | pppm             |
    | harmonic           | cosine_periodic  | harmonic        | harmonic         | nh_sphere     | pppm_tip4p       |
    | harmonic_shift_cut | cosine_shift_exp | ring            | helix            | nph_asphere   |                  |
    | harmonic_shift     | cosine_shift     | umbrella        | multi_harmonic   | nph           |                  |
    | morse              | cosine_squared   |                 | nharmonic        | nph_sphere    |                  |
    | nonlinear          | dipole           |                 | opls             | npt_asphere   |                  |
    | quartic            | fourier          |                 | quadratic        | npt           |                  |
    | table              | fourier_simple   |                 | table            | npt_sphere    |                  |
    |                    | harmonic         |                 |                  | nve           |                  |
    |                    | quartic          |                 |                  | nve_sphere    |                  |
    |                    | sdk              |                 |                  | nvt_asphere   |                  |
    |                    | table            |                 |                  | nvt           |                  |
    |                    |                  |                 |                  | nvt_sllod     |                  |
    |                    |                  |                 |                  | nvt_sphere    |                  |
    |                    |                  |                 |                  | peri_neigh    |                  |
    |                    |                  |                 |                  | qeq_comb      |                  |
    |                    |                  |                 |                  | qeq_reax      |                  |
    |                    |                  |                 |                  | rigid_nh      |                  |
    |                    |                  |                 |                  | rigid_nph     |                  |
    |                    |                  |                 |                  | rigid_npt     |                  |
    |                    |                  |                 |                  | rigid_nve     |                  |
    |                    |                  |                 |                  | rigid_nvt     |                  |
    |                    |                  |                 |                  | rigid         |                  |
    |                    |                  |                 |                  | rigid_small   |                  |

package-GPU
:   As of *3Mar20* version of LAMMPS, the following list of functionalities are available with the GPU package

{% include links.md %}
