#!/usr/local/anaconda3/bin/python
import argparse
import os
import pysam
parser = argparse.ArgumentParser( description='Put a description of your script here')
parser.add_argument('-s', '--sam_file', type=str, required=True, help='Path to an input file to be read' )
parser.add_argument('-o', '--out_file', type=str, required=False, help='Path to an input file to be read' )
parser.add_argument('-b', '--base', type=str, required=False, help='Path to an input file to be read' )
args = parser.parse_args()
if args.base:
	base=args.base
else:
	base="A"
if args.out_file:
	g=open(args.out_file,"w")
else:
	g=open(str(args.sam_file).split(".")[0]+"_" +str(base) + "train.tsv","w")
samfile = pysam.AlignmentFile(args.sam_file, "r")
context_list=[]
while True:
	try:
		reads1 = next(samfile)
		real_m=sum([i[1] for i in reads1.cigartuples if i[0]==7])
		x=sum([i[1] for i in reads1.cigartuples if i[0]==8])
		d=sum([i[1] for i in reads1.cigartuples if i[0]==1])
		i=sum([i[1] for i in reads1.cigartuples if i[0]==2])
		identiy=real_m/(real_m+d+i+x)
		pair=reads1.cigartuples
		if identiy >= 0.75 and reads1.query_alignment_length >=50:
			pre_pos_pair=reads1.get_aligned_pairs(matches_only=True)
			pos_pair=[j for j in pre_pos_pair if reads1.seq[j[0]]==base]
			reads_pos=[int(i[0]) for i in pos_pair]
			ref_pos=[i[1]+1 for i in pos_pair]
			ip=[str(i) for i in reads1.get_tag('ip')]
			pw=[str(i) for i in reads1.get_tag('pw')]
			for i in range(len(pos_pair)):
				if reads_pos[i]-10>=0 and reads_pos[i]+11<=len(reads1.seq):
					reads_context=reads1.seq[reads_pos[i]-10:reads_pos[i]+11]
					reverse_tag= 1 if reads1.is_reverse else 0
					if tuple([reads1.reference_name,ref_pos[i],reverse_tag]) not in context_list:
						print(reads1.reference_name,ref_pos[i],reverse_tag,reads_context,file=g)
						context_list.append(tuple([reads1.reference_name,ref_pos[i],reverse_tag]))	
				else:
					continue
	except StopIteration:
		break
g.close()
samfile.close()

