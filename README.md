# nobrainer-gear

This is a [Flywheel Gear](https://github.com/flywheel-io/gears/tree/master/spec) that wraps the [Nobrainer](https://github.com/neuronets/nobrainer) application for 3D image processing.

Nobrainer is a deep learning framework for 3D image processing. It implements several 3D convolutional models from recent literature, methods for loading and augmenting volumetric data that can be used with any TensorFlow or Keras model, losses and metrics for 3D data, and simple utilities for model training, evaluation, prediction, and transfer learning.

The default embedded models perform predictive masking of the brain in an MRI. Compatible models can be used to predict other areas of interest (e.g. brain tumors).

## Required inputs

1. **T1W**
    * T1-weighted anatomical volume (eg: MPRAGE)

## Optional inputs

1. **HDF5-Model**
    * nobrainer HDF5 Model, defaults to internally stored model.

## Configuration options

1. **threshold**
    * Threshold used to binarize model output. Only used in binary prediction and must be in (0, 1).
    * Defaults to `0.3`.
2. **largest-label**
    * Zero out all values not connected to the largest contiguous label (not including 0 values). This remove false positives in binary prediction.
    * Defaults to `False`
3. **rotate-and-predict**
    * Average the prediction with a prediction on a rotated (and subsequently un-rotated) volume. This can produce a better overall prediction with the expense of more time.
    * Defaults to `False`

## GPU Execution

Interactive docker sessions of this gear have been tested in a GPU environment with speedup in inference time (25 seconds (gpu) vs. 2 minutes (cpu)) on an NVIDIA GTX 1080 Ti.  Although all guest requirements are embedded within the docker container, this functionality is not enabled unless the host requirements are met.

Unfortunately, the host requirements necessary for GPU execution are not yet available on a Flywheel instance. They are scheduled to be available in early summer of 2020.

Local execution must be done with sample data, a valid configuration file (config.json), and the following nvidia container runtime command:
``nvidia-docker run --rm -v <local input directory>:<container input directory> -v <local config.json>:<container config.json> -v <local output directory>:<container output directory> <image id> ./run.py``

See Host and Container Requirements below:

### Host Requirements

1. NVIDIA Driver 410.48 was used in an ubuntu 18.04 (bionic). See [Driver Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/#binary-compatibility)
