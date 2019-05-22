# Use Python3 base
FROM python:3

# Move files to /tmp
COPY . /tmp

# Determines which HDF5 to build
ENV HDF5_MINOR_REL      hdf5-1.10.5 
ENV HDF5_SRC_URL   	http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10                  

# Build HDF5
RUN cd /tmp; \
	apt-get update && apt-get -y install gfortran libhdf5-serial-dev python-dev; \
	cd /tmp && ./build_hdf5; \
	pip install --no-binary=h5py h5py numpy; \
	rm -r /tmp/*
