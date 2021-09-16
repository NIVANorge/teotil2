# TEOTIL2 results files

This folder contains results from the annual TEOTIL2 modelling.

Column headings in the files are described below.

## TEOTIL2 (nutrients)

Files named `teotil2_results_{year}.csv`.

Columns named **accum_XXX** give fluxes from the specified regine catchment aggregating all inputs from that catchment and those upstream.

|             Column             | Description                                                                 |
|:------------------------------:|-----------------------------------------------------------------------------|
|  accum_agri_diff_tot-n_tonnes  | Agricultural diffuse   N                                                    |
|  accum_agri_diff_tot-p_tonnes  | Agricultural diffuse   P                                                    |
|   accum_agri_pt_tot-n_tonnes   | Agricultural point N                                                        |
|   accum_agri_pt_tot-p_tonnes   | Agricultural point P                                                        |
|  accum_all_point_tot-n_tonnes  | All point sources of   N i.e. Spredt + Aqua + Rense + Industry + Point Agri |
|  accum_all_point_tot-p_tonnes  | All point sources of   P i.e. Spredt + Aqua + Rense + Industry + Point Agri |
| accum_all_sources_tot-n_tonnes | All sources of N i.e.   All point + Anthropogenic diffuse + Natural diffuse |
| accum_all_sources_tot-p_tonnes | All sources of P i.e.   All point + Anthropogenic diffuse + Natural diffuse |
|  accum_anth_diff_tot-n_tonnes  | Anthropogenic diffuse   N i.e. Urban + Agricultural                         |
|  accum_anth_diff_tot-p_tonnes  | Anthropogenic diffuse   P i.e. Urban + Agricultural                         |
|     accum_aqu_tot-n_tonnes     | Aquaculture N                                                               |
|     accum_aqu_tot-p_tonnes     | Aquaculture P                                                               |
|     accum_ind_tot-n_tonnes     | Industry N                                                                  |
|     accum_ind_tot-p_tonnes     | Industry P                                                                  |
|   accum_nat_diff_tot-n_tonnes  | Natural diffuse N   i.e. Woodland + Upland + Lake + Agricultural background |
|   accum_nat_diff_tot-p_tonnes  | Natural diffuse P   i.e. Woodland + Upland + Lake + Agricultural background |
|          accum_q_m3/s          | Flow                                                                        |
|     accum_ren_tot-n_tonnes     | Renseanlegg N                                                               |
|     accum_ren_tot-p_tonnes     | Renseanlegg P                                                               |
|     accum_spr_tot-n_tonnes     | Spredt N                                                                    |
|     accum_spr_tot-p_tonnes     | Spredt P                                                                    |
|      accum_upstr_area_km2      | Total upstream   catchment area                                             |
|    accum_urban_tot-n_tonnes    | Urban N                                                                     |
|    accum_urban_tot-p_tonnes    | Urban P                                                                     |

 
Columns named **local_XXX** give fluxes from the specified regine catchment only i.e. not including inputs from upstream.
 
|             Column             | Description                                                                 |
|:------------------------------:|-----------------------------------------------------------------------------|
|         local_a_reg_km2        | Area of regine   "inter-catchment" i.e. not including upstream              |
|  local_agri_diff_tot-n_tonnes  | Agricultural diffuse   N                                                    |
|  local_agri_diff_tot-p_tonnes  | Agricultural diffuse   P                                                    |
|   local_agri_pt_tot-n_tonnes   | Agricultural point N                                                        |
|   local_agri_pt_tot-p_tonnes   | Agricultural point P                                                        |
|  local_all_point_tot-n_tonnes  | All point sources of   N i.e. Spredt + Aqua + Rense + Industry + Point Agri |
|  local_all_point_tot-p_tonnes  | All point sources of   P i.e. Spredt + Aqua + Rense + Industry + Point Agri |
| local_all_sources_tot-n_tonnes | All sources of N i.e.   All point + Anthropogenic diffuse + Natural diffuse |
| local_all_sources_tot-p_tonnes | All sources of P i.e.   All point + Anthropogenic diffuse + Natural diffuse |
|  local_anth_diff_tot-n_tonnes  | Anthropogenic diffuse   N i.e. Urban + Agricultural                         |
|  local_anth_diff_tot-p_tonnes  | Anthropogenic diffuse   P i.e. Urban + Agricultural                         |
|     local_aqu_tot-n_tonnes     | Aquaculture N                                                               |
|     local_aqu_tot-p_tonnes     | Aquaculture P                                                               |
|     local_ind_tot-n_tonnes     | Industry N                                                                  |
|     local_ind_tot-p_tonnes     | Industry P                                                                  |
|   local_nat_diff_tot-n_tonnes  | Natural diffuse N   i.e. Woodland + Upland + Lake + Agricultural background |
|   local_nat_diff_tot-p_tonnes  | Natural diffuse P   i.e. Woodland + Upland + Lake + Agricultural background |
|        local_q_reg_m3/s        | Flow                                                                        |
|     local_ren_tot-n_tonnes     | Renseanlegg N                                                               |
|     local_ren_tot-p_tonnes     | Renseanlegg P                                                               |
|       local_runoff_mm/yr       | Runoff for regine   unit                                                    |
|     local_spr_tot-n_tonnes     | Spredt N                                                                    |
|     local_spr_tot-p_tonnes     | Spredt P                                                                    |
|        local_trans_tot-n       | Regine transmission   factor for N                                          |
|        local_trans_tot-p       | Regine transmission   factor for P                                          |
|    local_urban_tot-n_tonnes    | Urban N                                                                     |
|    local_urban_tot-p_tonnes    | Urban P                                                                     |
|        local_vol_lake_m3       | Estimated lake volume for regine (not including upstream)                   |

## TEOTIL2 (metals)

Files named `teotil2_metals_results_{year}.csv`. Output is generated for the following metals: As, Cd, Cr, Cu, Hg, Ni, Pb and Zn (referred to by `{par}` in the tables below).

Columns named **accum_XXX** give fluxes from the specified regine catchment aggregating all inputs from that catchment and those upstream.

|             Column             | Description                                 |
|:------------------------------:|---------------------------------------------|
|  accum_all_point_{par}_tonnes  | All point sources of {par}                  |
|     accum_diff_{par}_tonnes    | All diffuse sources of {par}                |
| accum_all_sources_{par}_tonnes | All sources of {par} (i.e. point + diffuse) |
|     accum_ind_{par}_tonnes     | Industrial sources of {par}                 |
|     accum_ren_{par}_tonnes     | Renseanlegg sources of {par}                |
|          accum_q_m3/s          | Flow                                        |
|      accum_upstr_area_km2      | Total upstream catchment area               |

Columns named **local_XXX** give fluxes from the specified regine catchment only i.e. not including inputs from upstream.

|             Column             | Description                                                  |
|:------------------------------:|--------------------------------------------------------------|
|  local_all_point_{par}_tonnes  | All point sources of {par}                                   |
|     local_diff_{par}_tonnes    | All diffuse sources of {par}                                 |
| local_all_sources_{par}_tonnes | All sources of {par} (i.e. point + diffuse)                  |
|     local_ind_{par}_tonnes     | Industrial sources of {par}                                  |
|     local_ren_{par}_tonnes     | Renseanlegg sources of {par}                                 |
|        local_trans_{par}       | Regine transmission   factor for {par}                       |
|         local_a_reg_km2        | Area of regine "inter-catchment" i.e. not including upstream |
|        local_q_reg_m3/s        | Flow                                                         |
|       local_runoff_mm/yr       | Runoff for regine unit                                       |
|        local_vol_lake_m3       | Estimated lake volume for regine (not including upstream)    |