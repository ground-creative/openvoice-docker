 #!/bin/sh
if [ "${TEST}" ]; then 
	echo "Running Test";
	tail -f /dev/null;
else 
	echo "Running App";
	python3 /app/app.py;
fi
