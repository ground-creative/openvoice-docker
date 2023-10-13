 #!/bin/sh
if [ "${TEST}" = true ]; then 
	echo "Running test command \"tail -f /dev/null\"";
	tail -f /dev/null;
else 
	echo "Running command \"${COMMAND}\"";
	eval "${COMMAND}";
fi
