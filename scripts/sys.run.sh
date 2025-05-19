 #!/bin/sh
cd /

FIRST_RUN=false
VOLUME_PATH=$(realpath "$VOLUME")

install_openvoice_dependencies() {
 	# Install OpenVoice core dependencies
	echo "======= Installing OpenVoice core dependencies..."
	cd $VOLUME_PATH/OpenVoice
	pip install --break-system-packages --no-cache-dir -r requirements.txt
	# Install OpenVoice V2 checkpoints dependencies
	echo "======= Installing MeloTTS..."
	pip install git+https://github.com/myshell-ai/MeloTTS.git
	python -m unidic download
	# Export LD_LIBRARY_PATH
	export LD_LIBRARY_PATH=$(python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__) + ":" + os.getenv("LD_LIBRARY_PATH", ""))')
	echo 'export LD_LIBRARY_PATH=$(python3 -c "import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + \":\" + os.path.dirname(nvidia.cudnn.lib.__file__) + \":\" + os.getenv(\"LD_LIBRARY_PATH\", \"\"))")' >> ~/.bashrc
}

install_api_dependencies() {
	# Install API dependencies
	if [ -f "$VOLUME_PATH/api/requirements.txt" ]; then
		echo "======= Installing API dependencies..."
		cd $VOLUME_PATH/api
		pip install --break-system-packages --no-cache-dir -r requirements.txt
	fi
}

install_nltk_download() {
	if [ -z "$(ls -A "/opt/conda/envs/openvoice/nltk_data" 2>/dev/null)" ]; then
		python -m nltk.downloader -d '/opt/conda/envs/openvoice/nltk_data' all
	fi
}

# Add a 10-second sleep to debug start script
if [ "${TEST}" = true ]; then 
	echo "======= Test mode enabled, sleeping for 10 seconds..."
	sleep 10
fi

# Setup conda
. /opt/conda/etc/profile.d/conda.sh
if ! conda info --envs | grep -q openvoice; then
	FIRST_RUN=true
	echo "======= Setting up conda environment with python=${CONDA_PYTHON_VERSION}..."
    conda create -n openvoice python=${CONDA_PYTHON_VERSION} -y
	conda activate openvoice
	echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc
	echo "conda activate openvoice" >> ~/.bashrc
	export PYTHONPATH=$VOLUME_PATH:/app/OpenVoice
	echo "export PYTHONPATH=$VOLUME_PATH:/app/OpenVoice" >> ~/.bashrc
else
	conda activate openvoice
	export PYTHONPATH=/app:/app/OpenVoice
	export LD_LIBRARY_PATH=$(python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__) + ":" + os.getenv("LD_LIBRARY_PATH", ""))')
fi

# Check python version
python_version=$(python --version 2>&1)
echo "======= Current Python version: $python_version"

# Download OpenVoice
if [ -n "$OPENVOICE_REPOSITORY_URL" ]; then
 	if [ -z "$(ls -A "$VOLUME_PATH/OpenVoice" 2>/dev/null)" ]; then
		# Install OpenVoice core
		echo "======= Folder $VOLUME_PATH/OpenVoice is empty or does not exist, cloning OpenVoice repository...\n"
		git clone $OPENVOICE_REPOSITORY_URL $VOLUME_PATH/OpenVoice
		echo "\n-e .\nFlask[async]==3.0.3\ncolorlog==6.8.2" >> $VOLUME_PATH/OpenVoice/requirements.txt
		# Install OpenVoice v1 checkpoints
		echo "======= Installing OpenVoice v1 checkpoints"
		aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip -d $VOLUME_PATH/OpenVoice -o checkpoints_1226.zip
		unzip $VOLUME_PATH/OpenVoice/checkpoints_1226.zip -d $VOLUME_PATH/OpenVoice
		rm $VOLUME_PATH/OpenVoice/checkpoints_1226.zip
		# Install OpenVoice v2 checkpoints
		echo "======= Installing OpenVoice v2 checkpoints"
		aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip -d $VOLUME/OpenVoice -o checkpoints_v2_0417.zip
		unzip $VOLUME_PATH/OpenVoice/checkpoints_v2_0417.zip -d $VOLUME_PATH/OpenVoice
		rm $VOLUME_PATH/OpenVoice/checkpoints_v2_0417.zip
		if [ -n "$USRID" ] && [ -n "$GRPID" ]; then
			echo "======= Changing ownership of $VOLUME_PATH/OpenVoice to $USRID:$GRPID..."
			chown -R "$USRID:$GRPID" "$VOLUME_PATH/OpenVoice"
		fi
		if [ "${FIRST_RUN}" = false ]; then 
			install_openvoice_dependencies
		fi
	else
		echo "======= Folder $VOLUME_PATH/OpenVoice is not empty, skipping cloning OpenVoice repository..."
	fi
fi

# Download API
if [ -n "$API_REPOSITORY_URL" ]; then
 	if [ -z "$(ls -A "$VOLUME_PATH/api" 2>/dev/null)" ]; then
		# Install API
		echo "======= Folder $VOLUME_PATH/api is empty or does not exist, cloning API repository...\n"
		git clone $API_REPOSITORY_URL $VOLUME_PATH/api
		echo "\nFlask[async]==3.0.3\ncolorlog==6.8.2" >> $VOLUME_PATH/api/requirements.txt
		cp $VOLUME_PATH/api/env.sample $VOLUME_PATH/api/.env
		cp $VOLUME_PATH/api/tests/env.sample $VOLUME_PATH/api/tests/.env
		if [ -n "$USRID" ] && [ -n "$GRPID" ]; then
			echo "======= Changing ownership of $VOLUME_PATH/api to $USRID:$GRPID..."
			chown -R "$USRID:$GRPID" "$VOLUME_PATH/api"
		fi
		if [ "${FIRST_RUN}" = false ]; then 
			install_api_dependencies
		fi
	else
		echo "======= Folder $VOLUME_PATH/api is not empty, skipping cloning API repository..."
	fi
fi

# Install required dependencies if needed
if [ "${FIRST_RUN}" = true ]; then
	# Install OpenVoice dependencies
	install_openvoice_dependencies
	# Install API dependencies
	install_api_dependencies
	install_nltk_download
fi

# Run command
if [ "${TEST}" = true ]; then 
	echo "======= Running test command \"tail -f /dev/null\"";
	tail -f /dev/null;
else 
	# Add env vars to command
	COMMAND=$(echo "${COMMAND}" | sed "s/__SERVER_ADDRESS__/${SERVER_ADDRESS}/g; s/__SERVER_PORT__/${SERVER_PORT}/g")
	echo "======= Running command \"${COMMAND}\"";
	eval "${COMMAND}";
fi
