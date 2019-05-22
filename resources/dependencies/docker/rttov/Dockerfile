# Use Python3 base
FROM h5py:latest

# Copy RTTOV from local system
COPY . /tmp

# Set the working directory
WORKDIR /usr/src/app

# RTTOV variables
ENV LD_LIBRARY_PATH	/usr/local/hdf5/lib
ENV RTTOV_INSTALL_DIR	/usr/local/rttov12
ENV RTTOV_MINOR_REL	rttov123
ENV RTTOV_SRC_URL 	http://nwpsaf.eu/downloads/james

# Build the image
RUN cd /tmp && ./build_rttov; \
	rm -r /tmp/*
