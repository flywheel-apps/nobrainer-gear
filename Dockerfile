# Dockerfile exported by GearBuilderGUI.Stash edits before export again

# Inheriting from established docker image:
FROM kaczmarj/nobrainer:latest

# Inheriting from established docker image:
LABEL maintainer="Flywheel <support@flywheel.io>"

# Install APT dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    wget \ 
    zip && \ 
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install PIP Dependencies
RUN pip3 install --upgrade pip && \ 
    pip install \
    flywheel-sdk && \ 
    rm -rf /root/.cache/pip

# Specify ENV Variables
ENV \ 
    PATH=$PATH  \ 
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH 

# Make directory for flywheel spec (v0):
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

# Create directory for default model
RUN mkdir ${FLYWHEEL}/model && \
    cd ${FLYWHEEL}/model && \
    wget -nd https://github.com/neuronets/nobrainer-models/releases/download/0.1/brain-extraction-unet-128iso-model.h5 && \
    cd /
# Copy executable/manifest to Gear
COPY utils ${FLYWHEEL}/utils
COPY run.py ${FLYWHEEL}/run.py
COPY manifest.json ${FLYWHEEL}/manifest.json
RUN cd ${FLYWHEEL} && chmod a+x run.py

# ENV preservation for Flywheel Engine
RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w");json.dump(dict(os.environ), f)'

# Configure entrypoint
ENTRYPOINT ["/flywheel/v0/run.py"]