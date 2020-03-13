#!/bin/bash
#This file will teach you how to set up your condo environment to install pycairo and turn interleaved multiline fasta file into single line


#create new conda environment, call it pyci, indicate current python version
conda create -n pyci python=3.6

#activate pyci environment
conda activate pyci

#with new environment, you must install other packages that were in your "base" environment into the new environment (jupyter notebook, matplotlib...etc)
conda install jupyter
conda install -c conda-forge matplotlib

#to use pycairo, conda activate in working dir
Cd /Users/GioiTran/Documents/shell/Bi624/Motif_Mark
conda activate pyci

#to exit environment
Conda deactivate

#turn fasta interleaved fasta file into a single line fasta file
awk '{if(NR==1) {print $0} else {if($0 ~ /^>/) {print "\n"$0} else {printf $0}}}' Figure_1.fasta > new_Figure_1.fasta

#run Motif_Mark.py script
./Motif_Mark.py -f new_Figure_1.fasta -m Fig_1_motifs.txt
