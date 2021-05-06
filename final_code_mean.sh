export PATH=/home/yaoxinw/deep_learning/pacbio/software:$PATH
sta=$1
end=$2
file_tsv=$3
ipdratio_file=$4
wkd=$5
pre=$6
cd ${wkd}
awk '($2>='"$sta"')&&($2<'"$end"'){print}' ${file_tsv} > ${file_tsv}_${sta}_${end}_pos.tsv
compute_ipd_pw_mutiprocess.py -a ${ipdratio_file} -i ${file_tsv}_${sta}_${end}_pos.tsv -o ${wkd}/midresult_${sta}_${end} -f ${wkd}/${pre}_final_result_${sta}_${end} 
rm ${wkd}/midresult_${sta}_${end}
final_coding.py -i ${wkd}/${pre}_final_result_${sta}_${end} -o ${wkd}/${pre}_final_result_${sta}_${end}_coding.csv
awk -F ',' '$148==1{print}' ${wkd}/${pre}_final_result_${sta}_${end}_coding.csv > ${wkd}/${pre}_${sta}_${end}_coding1.csv
awk -F ',' '$148==0{print}' ${wkd}/${pre}_final_result_${sta}_${end}_coding.csv > ${wkd}/${pre}_${sta}_${end}_coding0.csv


