# PyRATE

## Python Radiometric Target Embedder

### Master's Thesis, JPohlmann, AFIT 2019

System for generating radiometric signatures of sub-pixel targets.
Designed with modularity in mind in order to simplify the trade off between speed and accuracy
as well as facilitate user customization.

The prospectus (WIP) for this project can be found [here](doc/prospectus/prospectus.pdf).

### Dependencies

- Python 3
  - Numpy
  - h5py
  - docker python sdk
- Docker

### Installation

Ensure that the above dependencies are installed before continuing.

Clone this repository and navigate to the main `pyrate/` directory.
Install the default plugins by running the `build_defaults.sh` script.
All Docker images should be automatically downloaded on the first run.
Note that the RTTOV Docker image is large and may take time to download.

### Potential issues

- Due to the dependence of this application on some shell scripts, functionality on Windows machines may be limited.
- Docker requires root (admin) privileges. If Docker errors are occuring, try the two options:
  1. Prepend the `sudo` command to the parent program or shell.
  2. Add the user to the `docker` group using `sudo usermod -a -G docker <user>`.
