#!/bin/bash
# Build dependencies (if necessary)

# Move RTTOV profiles
tar -xzf ./resources/dependencies/data/rttov-profiles.tar.gz -C ./resources/plugins/atmosphere/rttov/app/

# Download IASI profile
RTCOEF_IASI_SRC=https://www.nwpsaf.eu/downloads/rtcoef_rttov12/rttov9pred101L/rtcoef_metop_2_iasi.H5
wget -P ./resources/plugins/atmosphere/rttov/app/rtcoef_rttov12/rttov9pred101L $RTCOEF_IASI_SRC
