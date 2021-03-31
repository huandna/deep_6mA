#!/usr/local/anaconda3/bin/python
import argparse
import os
import pysam
parser = argparse.ArgumentParser( description='Put a description of your script here')
parser.add_argument('-a', '--m6a_file', type=str, required=True, help='Path to an input file to be read' )
parser.add_argument('-c', '--csv_file', type=str, required=False, help='Path to an input file to be read' )
parser.add_argument('-r', '--refseq', type=str, required=False, help='Path to an input file to be read' )
parser.add_argument('-o', '--out_file', type=str, required=False, help='Path to an input file to be read' )
args = parser.parse_args()
if args.out_file:
	g=open(args.out_file,"w")
else:
	g=open(str(args.sam_file).split(".")[0]+"_" +str(base) + "train.tsv","w")
m6A=[]
ipdratio_dic={}
seq=pysam.FastaFile(args.refseq)
def DNA_complement_and_reverse(sequence):
    sequence=sequence.upper()
    transline=sequence[::-1].replace('A','t').replace('T','a').replace('G','c').replace('C','g').upper()
    return transline
with open(args.m6a_file) as f:
	for line in f.readlines():
		line=line.strip().split(",")
		if line[2]=="m6A":
			line[6]  =  0  if  line[6]=="+"  else  1  
			m6A.append(tuple([line[0],line[3],line[6]]))		
with open(args.csv_file) as f:
	for line in f.readlines()[1:]:
		line=line.strip().split(",")
		line[0]=line[0].strip("\"")
		if line[3]=="A":
			ID=tuple([line[0],line[1],int(line[2])])
			seq.get_reference_length(ID[0])
			start1=int(ID[1])-11
			end1=int(ID[1])+10
			reflength=seq.get_reference_length(ID[0])
			if start1>0 and end1<reflength:
				context=seq.fetch(reference=ID[0], start=start1, end=end1)
			else:
				context="CC"
			context=context.upper() if ID[2]==0 else DNA_complement_and_reverse(context)
			if ID in m6A:
				ipdratio_dic[ID]=[line[8],1]
			else:
				ipdratio_dic[ID]=[line[8],0]
			print(ID[0],ID[1],ID[2],ipdratio_dic[ID][0],ipdratio_dic[ID][1],context,file=g)		
		else:
			continue
#  there is only "=" and no "m" in this bam version 

