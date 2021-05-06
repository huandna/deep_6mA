#!/usr/local/anaconda3/bin/python
import argparse
import os
import pysam
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

parser = argparse.ArgumentParser( description='Put a description of your script here')
parser.add_argument('-i', '--ipd_file', type=str, required=False, help='Path to an input file to be read' )
parser.add_argument('-a', '--m6a_file', type=str, required=False, help='Path to an input file to be read' )
parser.add_argument('-o', '--out_file', type=str, required=False, help='Path to an input file to be read' )
parser.add_argument('-f', '--final_file', type=str, required=False, help='Path to an input file to be read' )
args = parser.parse_args()
data = pd.read_csv(args.ipd_file,sep=" ",names=["chr","pos","flag","ipd","pw"])
g=open(args.out_file,"w") 
data.set_index(["chr","pos","flag"],inplace=True)
for i in data.index.levels[0]:
    data1=data.loc[i]
    for j in set([p[0] for p in data1.index]):
            data2=data1.loc[j]
            for f in set(data2.index):
                if len(data2.loc[f]) >=5:
                    tensoripd=np.array(data2.loc[f].ipd)
                    tensorpw=np.array(data2.loc[f].pw)
                    ipd="-".join(str(n) for n in list(tensoripd))
                    pw="-".join(str(n) for n in list(tensorpw))
                    print(i,j,f,ipd,pw,file=g)
                else:
                    continue
g.close()

def get_mean(list1):
    list1=[int(i) for i in list1.split("-")]
    return np.mean(list1)
def compute_mean(piece):
    col1=get_mean(piece["ipd_list"])
    col2=get_mean(piece["pw_list"])
    return [col1,col2]
del data
data2=pd.read_csv(args.out_file,sep=" ",names=["chr","pos","flag","ipd_list","pw_list"])
data2.set_index(["chr","flag","pos"],inplace=True) 
temp=data2.apply(compute_mean,axis=1)
data2[["ipd_mean","pw_mean"]]=list(map(np.array,temp))
colname1=["ipd_mean"+str(i) for i in range(21)]
colname2=["pw_mean"+str(i) for i in range(21)]
data2 = pd.concat([data2, pd.DataFrame(columns=colname1+colname2)])
for chrname in data2.index.levels[0]:
    data_chr=data2.loc[chrname]
    for strand in set([p[0] for p in data_chr.index]):
            data_strand=data_chr.loc[strand]
            for pos in set(data_strand.index):
                  data2.loc[(chrname,strand,pos),colname1+colname2]=[data_strand.loc[i].ipd_mean if i in data_strand.index else 0  for i in range(pos-10,pos+11)]+[data_strand.loc[i].pw_mean if i in data_strand.index else 0  for i in range(pos-10,pos+11)]
data2=data2.reset_index()
data2.set_index(["chr","pos","flag"],inplace=True) 
 
data1 = pd.read_csv(args.m6a_file,sep=" ",names=["chr","pos","flag","ipdratio","6ma_flag","context"])
data1.set_index(["chr","pos","flag"],inplace=True)

df_final=pd.concat([data2,data1],axis=1, join='inner')
df_final=df_final.reset_index()
df_final.set_index(["chr","pos","flag","6ma_flag"],inplace=True)
df_final.to_csv(args.final_file)



