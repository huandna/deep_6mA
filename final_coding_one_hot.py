#!/usr/local/anaconda3/bin/python
import argparse
import os
import pysam
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
def get_DNA_seq_tensor(seq):
    seq=seq.upper()
    df=np.zeros((4,len(seq)),dtype="int")
    df = pd.DataFrame(df,index=["A","T","C","G"])
    for i in range(len(seq)):
        df.loc[seq[i],i]=1 
    return np.array(df).reshape(1,-1)[0]
def re_code(piece):
    col1=get_cluster([int(i) for i in piece["ipd_list"].split("-")],5)
    col2=get_cluster([int(i) for i in piece["pw_list"].split("-")],5)
    col3=list(get_DNA_seq_tensor(piece["context"]))
    return col1+col2+col3
def get_cluster(tensor,n):
    result1=[]
    result2=[]
    if len(set(tensor)) <n:
        tensor.sort()
        result1=tensor[int((len(tensor)-5)/2):int((len(tensor)-5)/2)+5]
        result2=[0,0,0,0,0]
    else:
        y = np.array(tensor).reshape(-1, 1)
        km = KMeans(n_clusters=n,random_state=1)
        km.fit(y)
        for i in range(n):
            result1.append(np.mean(y[km.labels_==i]))
            result2.append(np.std(y[km.labels_==i]))
    result1.sort()
    result2.sort()
    return result1+result2


parser = argparse.ArgumentParser( description='Put a description of your script here')
parser.add_argument('-i', '--in_file', type=str, required=False, help='Path to an input file to be read' )
parser.add_argument('-o', '--out_file', type=str, required=False, help='Path to an input file to be read' )
args = parser.parse_args()
df_final=pd.read_csv(args.in_file,sep=",",names=["chr","pos","flag","6ma_flag","ipd_list","pw_list","ipdratio","context"],header=1)
colname1=["clu_ipd"+str(i) for i in range(10)]
colname2=["clu_pw"+str(i) for i in range(10)]
colname3=["code"+str(i) for i in range(84)]
df_final = pd.concat([df_final, pd.DataFrame(columns=colname1+colname2+colname3)])
temp=df_final.apply(re_code,axis=1)
df_final[colname1+colname2+colname3]=pd.DataFrame(list(map(np.array,temp)))
df_final["final_tag"]=df_final["6ma_flag"]
df_final["final_tag"]=df_final["final_tag"].astype(int)
df_final=df_final.drop(['chr', 'pos', 'flag', '6ma_flag', 'context','ipd_list', 'pw_list',],axis=1)
df_final=df_final.round(3)
df_final.to_csv(args.out_file,header=False,index=False)




