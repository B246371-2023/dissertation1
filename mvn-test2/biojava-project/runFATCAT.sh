#!/bin/bash

# examples:

#  bash runFATCAT.sh -pdb1 4hhb.A -pdb2 4hhb.B -pdbFilePath /tmp/ -autoFetch -show3d 
#  bash runFATCAT.sh -pdb1 4hhb.A -pdb2 4hhb.B -pdbFilePath /tmp/ -printXML 
#  bash runFATCAT.sh -pdb1 4hhb.A -pdb2 4hhb.B -pdbFilePath /tmp/ -printFatCat
# 
#  run a flexible alignment:
#  bash runFATCAT.sh -pdb1 4hhb.A -pdb2 4hhb.B -pdbFilePath /tmp/ -printFatCat -flexible 
# 
# for more examples see runCE.sh
# jCE works almost exactly the same...


### Execute jar ###


# Get the base directory of the argument.
# Get the base directory of the argument.
# Can resolve single symlinks if readlink is installed
LIB_PATH=/home/s2530615/dissertation/biojava-protein-comparison-tool-4.0.0/lib
# send the arguments to the java app
java -Xmx500M -cp "$LIB_PATH/*:." org.biojava.nbio.structure.align.fatcat.FatCat "$@"
