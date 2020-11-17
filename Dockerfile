ARG BASE_CONTAINER=jupyter/minimal-notebook:612aa5710bf9
FROM $BASE_CONTAINER

LABEL maintainer="James Sample <james.sample@niva.no>"

USER root

# OS dependencies =================================================================================
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gdebi-core \
    software-properties-common && \
    rm -rf /var/lib/apt/lists/*
    
RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable && \
    apt-get update && \
    apt-get install -y \
    gdal-bin \ 
    graphviz \
    libgdal-dev \
    libgeos-dev \
    libgraphviz-dev \
    libgsl-dev \
    libproj-dev \
    libspatialindex-dev \
    libudunits2-dev \
    proj-bin \
    proj-data && \
    rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

# Python packages =================================================================================
RUN python -m pip install pip --upgrade --no-cache-dir && \
    rm -rf /tmp/* 
    
RUN python -m pip install --no-cache-dir \
    'numpy' && \
    rm -rf /tmp/* 
    
COPY ./requirements.txt /tmp/
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp/* 
    
# Install TEOTIL2 =================================================================================
WORKDIR /teotil2
COPY ./setup.py /teotil2/
COPY ./README.md /teotil2/
COPY ./requirements.txt /teotil2/
COPY ./LICENSE /teotil2/
COPY ./teotil2/ /teotil2/teotil2
RUN python setup.py install
WORKDIR $HOME 
    
# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID 