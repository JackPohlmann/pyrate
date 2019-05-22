#!/bin/bash
# Build dependencies (if necessary)

# Move RTTOV profiles
echo "Unpacking RTTOV profiles..."
tar -xzf ./resources/dependencies/data/rttov-profiles.tar.gz -C ./resources/plugins/atmosphere/rttov/app/

# Make RTTOV Controller
echo "Making RTTOV Controller..."
mkfifo ./resources/plugins/atmosphere/rttov/app/controller

# Download IASI profile
echo "Downloading RTTOV IASI coefficients..."
RTCOEF_IASI_SRC=https://www.nwpsaf.eu/downloads/rtcoef_rttov12/rttov9pred101L/rtcoef_metop_2_iasi.H5
IASI_INSTALL_DIR=./resources/plugins/atmosphere/rttov/app/rtcoef_rttov12/rttov9pred101L
if [[ "$OSTYPE" == "linux-gnu" ]]; then
	wget -P $IASI_INSTALL_DIR $RTCOEF_IASI_SRC
elif [[ "$OSTYPE" == "darwin"* ]]; then
	(cd $IASI_INSTALL_DIR && curl -O $RTCOEF_IASI_SRC)
	ec=$?
	while [[ $ec == 18 ]]; do
		echo "Resuming download..."
		(cd $IASI_INSTALL_DIR && curl -O -C - $RTCOEF_IASI_SRC)
		ec=$?
	done
elif [[ "$OSTYPE" == "cygwin" ]]; then
	wget -P $IASI_INSTALL_DIR $RTCOEF_IASI_SRC
elif [[ "$OSTYPE" == "msys" ]]; then
	(cd $IASI_INSTALL_DIR && curl -O $RTCOEF_IASI_SRC)
	ec=$?
	while [[ $ec == 18 ]]; do
		echo "Resuming download..."
		(cd $IASI_INSTALL_DIR && curl -O -C - $RTCOEF_IASI_SRC)
		ec=$?
	done
fi

echo "Finished."
