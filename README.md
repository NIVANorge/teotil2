# TEOTIL2 - A simple model for estimating riverine fluxes

TEOTIL2 is a simple, export-coefficient-based model for estimating riverine fluxes. The model makes it easy to define a catchment network, assign local inputs to subcatchments, and accumulate fluxes downstream (allowing for retention in subcatchments, if desired).

The original TEOTIL model for nutrients (total nitrogen and phosphorus) was developed by [Tjomsland *et al*. (2010)](https://niva.brage.unit.no/niva-xmlui/handle/11250/214825) and has been widely used in Norway for simulating nutrient fluxes at national scale - for example as part of Miljødirektoratet's [Elveovervåkingsprogrammet](https://github.com/JamesSample/rid) and for reporting to the [OSPAR Commission](https://www.ospar.org/).

This repository contains a Python implementation TEOTIL, named TEOTIL2. The new version of the model has a more flexible and generic structure, but uses broadly the same input datasets as previously and aims to recreate outputs from the original model as closely as possible (see the links below for a comparison). All calculations have been restructured using [networkx](https://networkx.org/) to significantly improve computational performance.

This repository also includes code for **TEOTIL2 Metals**, an extension of the original model that uses broadly the same principles to simulate fluxes of arsenic (As), cadmium (Cd), copper (Cu), chromium (Cr), lead (Pb), mercury (Hg), nickel (Ni) and zinc (Zn).

All the examples make use of Norway's ["regine" catchment network](https://kartkatalog.geonorge.no/metadata/regine-enhet/8721cdac-f959-4adc-9d54-d3b770e5fa1e) for flux calculations at national scale, but the model can also be used with user-specified catchments.

<p align="center">
  <img src="images/teotil2_example.png" alt="TEOTIL2 example" width="800" />
</p>

## Installation


## Documentation and tutorials

 * **[TEOTIL2 basic concepts](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/01_teotil2_basics.ipynb)**. A brief overview of key concepts in TEOTIL2: how input files are structured, how fluxes are calculated, how to explore model ouput and how to extend the model to simulate additional parameters.

 * **[Introduction to TEOTIL2 (nutrients)](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/02_teotil2_nutrients.ipynb)**. Illustrating use of the new model to simulate annual nutrient fluxes for Norway's "regine" catchment network (~20,000 catchments nationally). This notebook also compares output from the new model for 2015 with results from the original TEOTIL model for the same year
 
 * **[Running the model for multiple years](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/03_run_nutrients_all_years.ipynb)**. Running TEOTIL2 Nutrients for a user-specified range of years to produce output in a consistent format

## Reports and technical information

 * **[Original report for TEOTIL (version 1) by Tjomsland *et al*. (2010)](https://niva.brage.unit.no/niva-xmlui/handle/11250/214825)**. An introduction to the original model, including example applications

## Development notebooks