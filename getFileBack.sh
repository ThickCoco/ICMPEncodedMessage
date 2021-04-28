#!/bin/bash

if [ -z "$1"  ]
then

	echo "Introduce un nombre para darle al fihcero donde guardar los datos"

else

	python jsonAnalyzer.py > hexFile
	cat hexFile | xxd -r -p > ofBase64
	python deOfuscador.py ofBase64 base64File
	cat base64File | base64 -d > $1
	rm base64File
	rm ofBase64
	rm hexFile

fi
