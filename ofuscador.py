#!/usr/bin/python


import sys, os


if len(sys.argv) != 3:
    print "Numero erroneo de argumentos"
    print "arg1: fichero en base64 para obfuscar"
    print "arg2: fichero que sera el output"
    sys.exit()

inF = sys.argv[1]
outF = sys.argv[2]

os.system('rm -f ' + outF)
os.system('echo "" > ' + outF)


inFile = open(inF, 'r')
outFile = open(outF, 'w')


while 1:
    inChar = inFile.read(1)

    if not inChar:
        break

    if inChar != '\n':
        outChar = ord(inChar) + 1
	outChar = chr(outChar)

        if outChar == ':':
            outChar = '0'
        if outChar == '{':
            outChar = 'a'
        if outChar == '[':
            outChar = 'A'

    else:
        outChar = inChar

    outFile.write(outChar)


inFile.close()
outFile.close()


outFile = open(outF, 'r')
str = outFile.read()
str = str.rstrip()
outFile.close()

outFile = open(outF, 'w')
outFile.write(str)
outFile.close()






