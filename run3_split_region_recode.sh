export PATH=/home/yaoxinw/deep_learning/pacbio/software:$PATH
bac=$1
wkd=/home/yaoxinw/deep_learning/pacbio/all_bacteria/${bac}
ref=/home/yaoxinw/bacteria/ref_assembly/${bac}/${bac}_pb.fasta
cd ${wkd}
#######################       split genome region for computing and  merge ipdratio&context       ###########################
#for((i=1;i<=5000000;i=i+20000));do end=$(echo $i+20000 | bc);echo $i $end;done > ${wkd}/region_list
grep '>' $ref | sed -n 's/>//p' > chr_list
for i in $(cat ${wkd}/chr_list);
do
#awk '$1=="'"$i"'"{print}' ${wkd}/all_a.tsv > ${i}_all_a.tsv
awk '{print $1;print$2}' ${wkd}/region_list | parallel --max-args=2 -j 40 final_code.sh {1} {2} ${i}_all_a.tsv ${wkd}/new_only_A_merge.tsv $wkd ${i}
done
######################       finish final train_data ###########################
cat ${wkd}/*coding1.csv > positive_data
cat ${wkd}/*coding0.csv > negative_data



