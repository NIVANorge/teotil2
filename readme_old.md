# TEOTIL2

This repository contains a Python implementation of the **TEOTIL** nutrient export model of [Tjomsland *et al*. (2010)](https://niva.brage.unit.no/niva-xmlui/handle/11250/214825). This model has been widely used in Norway for simulating nutrient fluxes (nitrogen and phosphorus) at national scale, for example as part of Miljødirektoratet's [Elveovervåkingsprogrammet](https://github.com/JamesSample/rid) and for reporting to the [OSPAR Commission](https://www.ospar.org/).

The new version of the model has a more flexible and generic structure, but uses broadly the same input datasets as previously and aims to recreate outputs from the original model as closely as possible (see the links below for a comparison). All calculations have been restructured using [networkx](https://networkx.org/) to significantly improve computational performance.

This repository also includes prototype code for **TEOTIL2 Metals**, an extension module that uses broadly the same principles to simulate fluxes of arsenic (As), cadmium (Cd), copper (Cu), chromium (Cr), lead (Pb), mercury (Hg), nickel (Ni) and zinc (Zn).

## TEOTIL2 introduction

 * **[TEOTIL2 basic concepts](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/01_teotil2_basics.ipynb)**. A brief overview of key concepts in TEOTIL2: how input files are structured, how fluxes are calculated, how to explore model ouput and how to extend the model to simulate additional parameters.

 * **[Introduction to TEOTIL2 (nutrients)](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/02_teotil2_nutrients.ipynb)**. Illustrating use of the new model to simulate annual nutrient fluxes for Norway's "regine" catchment network (~20,000 catchments nationally). This notebook also compares output from the new model for 2015 with results from the original TEOTIL model for the same year
 
 * **[Running the model for multiple years](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/03_run_nutrients_all_years.ipynb)**. Running TEOTIL2 Nutrients for a user-specified range of years to produce output in a consistent format
 
## TEOTIL2 applications

TEOTIL2 (nutrients) has been used since 2016 to simulate nutrient fluxes for "unmonitored regions" as part of [Elveovervåkingsprogrammet](https://github.com/JamesSample/rid). The links below refer to the notebooks from 2018/19 (i.e. 2018 data; analysis performed during 2019), but similar notebooks for all years since 2016 are listed [here](https://github.com/JamesSample/rid).

 * **[Processing annual input datasets](https://nbviewer.jupyter.org/github/JamesSample/rid/blob/master/notebooks/process_model_inputs_2018.ipynb)**. Restructuring the land use, sewage, industry and fish farm datasets for 2018 and adding them to NIVA's database
 
 * **[Estimating nutirent loads for unmonitored areas](https://nbviewer.jupyter.org/github/JamesSample/rid/blob/master/notebooks/loads_unmonitored_regions_2018.ipynb)**. Using the model to estimate N and P fluxes in unmonitored regions for 2018. These data are used to support OSPAR reporting
 
## TEOTIL2 Metals (work in progress)

Model development and prototype code for a new metals module for TEOTIL2, to be added during 2020.

 * **[Initial data exploration and prototyping](https://nbviewer.jupyter.org/github/JamesSample/rid/blob/master/notebooks/nope_metals_3.ipynb)**. This is the original TEOTIL2-Metals notebook from late 2018, which uses data from the 1995 "1000 Lakes" survey to assess the feasibility of a new TEOTIL metals module. Based on this notebook, it was agreed with Miljødirektoratet to delay development of the new module until after the 2019 "1000 Lakes" survey was completed. It is ghoped that improvements in laboratory limits of quantification (LOQs) for the more recent survey will make it easier to convincingly derive key relationships
 
 * **[Spatial interpolation of key metals datasets](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/04_spatial_interpolation.ipynb)**. Interpolating water chemistry, moss and geochemistry datasets onto a common spatial grid
 
 * **[Exploring the 2019 "1000 Lakes" dataset](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/2019_1000_lakes.ipynb)**. Repeating parts of the analysis above using the 2019 "1000 Lakes" dataset to see if improved laboratory limits of quantification can help with deriving model coefficients
 
 * **[TEOTIL2-Metals part 1](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/05_teotil2_metals_pt1.ipynb)**. Creating the basic structure of a metals module and testing to see if a naive approach (without retention or rigorously justified export coefficients) can nevertheless perform better than the current approach (which ignores diffuse background contributions and only considers point discharges) 
 
 
