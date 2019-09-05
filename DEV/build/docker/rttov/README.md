# RTTOV Docker image

Builds RTTOV Docker image with python wrapper and hdf5 functionality.

## Instructions

Docker must be installed first.
Once installed, please check the OS-specific instructions for starting Docker.
Clone this repository and enter the directory.

### Pre-installation

Make sure the desired options are set within the `opts` script before building the image.
The default image will compile RTTOV 12.3 against HDF5 1.10.5.

### Installation

The Docker image can be built by simply running:

```
sudo docker build --tag=rttov .
```

The installation directory of RTTOV is, by default, `/usr/local/rttov12`.

### After installation

Once built, the image can be tested with:

```
$ sudo docker run --rm -it rttov bash
root@<docker-id>: cd /usr/local/rttov12/rttov_test
root@<docker-id>: ./test_rttov12.sh ARCH=gfortran
```

Alternatively, one can simply enter a Python shell by running the `python` command within bash or by initiating a Python shell with `$ sudo docker run --rm -it rttov python` and importing `pyrttov`.
The Docker container can be exited as any normal shell and will automatically terminate as this was indicated by the `--rm` option.

## Notes

This is a "raw" docker image: it does not run any specific application nor does it have a default directory.
The foremost purpose of this image is to use it as a base image for external applications.

### Coefficient files

This RTTOV installation does not have any coefficient files aside from the defaults.
Specific device coefficient files can be mounted to the docker container and moved to the appropriate folders.
Alternatively, the coefficient files can be built into the image by running the `download_rttov` script before building the image and placing the desired files into the appropriate folders before continuing with the regular image build process.

### Atlases

This docker image is built without any surface emissivity/BRDF atlases.
These can be installed in a similar manner to the coefficient files.
