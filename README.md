# TEOTIL2
## A simple model for estimating riverine fluxes

TEOTIL2 is a simple, export-coefficient-based model for estimating riverine fluxes. The model makes it easy to define a catchment network, assign local inputs to subcatchments, and accumulate fluxes downstream (allowing for retention in subcatchments, if desired).

The original TEOTIL model for nutrients (total nitrogen and phosphorus) was developed by [Tjomsland *et al*. (2010)](https://niva.brage.unit.no/niva-xmlui/handle/11250/214825) and has been widely used in Norway for simulating nutrient fluxes at national scale - for example as part of Miljødirektoratet's [Elveovervåkingsprogramme](https://github.com/JamesSample/rid) and for reporting to the [OSPAR Commission](https://www.ospar.org/).

This repository contains a Python implementation TEOTIL, named TEOTIL2. The new version of the model has a more flexible and generic structure, but uses broadly the same input datasets as previously and aims to recreate outputs from the original model as closely as possible (see [here](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/02_teotil2_nutrients.ipynb#4.-Comparison-to-the-original-TEOTIL) for a comparison). All calculations have been restructured using [networkx](https://networkx.org/) to significantly improve computational performance.

This repository also includes code for **TEOTIL2 Metals**, an extension of the original model that uses the same principles to simulate fluxes of arsenic (As), cadmium (Cd), copper (Cu), chromium (Cr), lead (Pb), mercury (Hg), nickel (Ni) and zinc (Zn).

All the examples in this repository make use of Norway's ["regine" catchment network](https://kartkatalog.geonorge.no/metadata/regine-enhet/8721cdac-f959-4adc-9d54-d3b770e5fa1e) for flux calculations at national scale, but the model can also be used with user-specified catchments if desired.

<p align="center">
  <img src="images/teotil2_example.png" alt="TEOTIL2 example" width="800" />
</p>

## Installation

The easiest way to use TEOTIL2 is via [NIVA's JupyterHub](jupyterhub.niva.no) - please contact [James Sample](https://www.niva.no/Ansatte/james-edward-sample) if you would like to discuss access. Alternatively, you can install the model yourself and then either create your own input files or work with the pre-built files provided in this repository (see [here](https://github.com/NIVANorge/teotil2/tree/main/data/norway_annual_input_data)).

The TEOTIL2 model itself is a simple, pure Python package, but it has some more complex non-Python dependencies ([GDAL](https://gdal.org/), [PROJ](https://proj.org/) and [Graphviz](https://graphviz.org/)) that must be installed first. If you're using Linux everything should be straightforward, but Windows users may find installing these dependencies more tricky.

### Docker (recommended)

The recommended way to run TEOTIL2 yourself - regardless of your operating system - is by using Docker to extend one of the [Jupyter Docker Stacks](https://github.com/jupyter/docker-stacks). First build the Dockerfile in this repository using e.g.

    docker build -t teotil2 .
    
and then run it using e.g.

    docker run -ti --rm -p 8888:8888 -v ${PWD}:/home/jovyan/work teotil2 start.sh jupyter lab
    
You can now open a new browser tab, navigate to `http://127.0.0.1:8888/lab?` and begin using JupyterLab.

### Linux

First install the non-python dependencies using your system package manager and then install TEOTIL2 using `pip`

    python -m pip install --no-cache-dir git+https://github.com/NIVANorge/teotil2.git
    
The full repository is quite large, so afterwards you may wish to clean up your `tmp` directory

    rm -rf /tmp/* 

See the [Dockerfile](https://github.com/NIVANorge/teotil2/blob/main/Dockerfile) for full details of how to install on Ubuntu.

### Windows

Installing the dependencies on Windows can either be done manually (requires a compiler to be installed) or using a package manager such as [Conda](https://docs.conda.io/en/latest/), then install TEOTIL2 via `pip`, as shown above. Note that you need to make sure your `PATH` environment variable is correctly configured so the Python packages are able to find the non-Python libraries.

## Documentation and tutorials

The easiest way to get started with TEOTIL2 is by working through some practical examples. The notebooks below demonstrate how to run the model in different modes (e.g. `metals` versus `nutrients`) and how to explore the output.

 * [Tutorial 01: TEOTIL2 basic concepts](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/01_teotil2_basics.ipynb)

 * [Tutorial 02: An introduction to TEOTIL2 (nutrients)](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/02_teotil2_nutrients.ipynb)
 
 * [Tutorial 03: Running TEOTIL2 (nutrients) for multiple years](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/03_run_nutrients_all_years.ipynb)
 
 * [Tutorial 04: An introduction to TEOTIL2 (metals)](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/04_teotil2_metals.ipynb)
 
 * [Tutorial 05: Running TEOTIL2 (metals) for multiple years](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/05_run_metals_all_years.ipynb)
 
 * [Tutorial 06: Explore time series from TEOTIL2 (metals)](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/06_explore_teotil2_metals_output.ipynb)

## Reports and technical information

The links below provide additonal background information, theory and technical details for TEOTIL models.

 * [Report for the original TEOTIL model (version 1) by Tjomsland *et al*. (2010)](https://niva.brage.unit.no/niva-xmlui/handle/11250/214825)
 
 * [TEOTIL2 (metals) development report (2020)](https://nivanorge.github.io/teotil2/pages/00_intro_and_toc.html)

## Development notebooks

These notebooks document development of TEOTIL2 Metals, beginning with initial data exploration and interpolation.

 * [Metals development 01: Interpolation of datasets and preliminary statistical analysis](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/dev02_teotil2_metals_interp_and_regress.ipynb)
 
 * [Metals development 02: Incorporating the 2019 "1000 Lakes" dataset](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/dev03_teotil2_metals_1k_lakes_2019.ipynb)
 
 * [Metals development 03: Exploring changes over time](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/dev04_teotil2_metals_over_time.ipynb)