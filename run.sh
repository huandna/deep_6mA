export PATH=/home/yaoxinw/deep_learning/pacbio/software:$PATH
bac=$1
wkd=/home/yaoxinw/deep_learning/pacbio/all_bacteria/${bac}
ref=/home/yaoxinw/bacteria/ref_assembly/${bac}/${bac}_pb.fasta
cd ${wkd}
ln -s /home/yaoxinw/bacteria/process/${bac}/all_ipd.bam ${wkd}
ln -s /home/yaoxinw/bacteria/process/${bac}/modifications.gff.gz ${wkd}
ln -s /home/yaoxinw/bacteria/process/${bac}/modifications.csv.gz ${wkd}
############################### split_sam ########################################
HEAD_NUMBER=$(samtools view -h ${wkd}/all_ipd.bam | head -n 100 | grep -n -w @PG | tail -n 1 | awk -F ':' '{print $1}')
samtools view -h ${wkd}/all_ipd.bam | head -n $HEAD_NUMBER > ${wkd}/sam_head
samtools view ${wkd}/all_ipd.bam > ${wkd}/all_ipd.sam
mkdir -p ${wkd}/split_sam
split -d -n l/100 ${wkd}/all_ipd.sam ${wkd}/split_sam/splitsam
for i in $(ls "$wkd"/split_sam/splitsam*);
do 
cat ${wkd}/sam_head $i > ${i}_new.sam
rm ${i}
done
####################### compute_ipd_&_pw_for_every_base_site###########################
ls ${wkd}/split_sam/*_new.sam | parallel -j 40 --max-args=1 create_IPD_from_sam.py -s {1} -o {1}.tsv
rm ${wkd}/*_new.sam
cat ${wkd}/split_sam/*.tsv > ${wkd}/all_a.tsv
#######################       prepare_ipdratio_data         ###########################
zcat ${wkd}/modifications.gff.gz | grep -v "##" - | sed 's/ /\t/g' | sed 's/coverage=//' | sed 's/;IPDRatio=/\t/' | sed 's/;context=/\t/' | sed 's/;frac=/\t/' | sed 's/;fracLow=/\t/' | sed 's/;fracUp=/\t/' | sed 's/;identificationQv=/\t/' | sed 's/\t/,/g' > m6A.gff 
zcat ${wkd}/modifications.csv.gz > modifications.csv
merge_modicatoin_gff_csv.py -a ${wkd}/m6A.gff -c ${wkd}/modifications.csv -o only_a.merge.tsv -r $ref
awk '$6!="CC"{print}' only_a.merge.tsv | awk '$6!="GG"{print}' - > new_only_A_merge.tsv

#######################       split genome region for computing and  merge ipdratio&context       ###########################
for((i=1;i<=5000000;i=i+20000));do end=$(echo $i+20000 | bc);echo $i $end;done > ${wkd}/region_list
grep '>' $ref | sed -n 's/>//p' > chr_list
for i in $(cat ${wkd}/chr_list);
do
awk '$1=="'"$i"'"{print}' ${wkd}/all_a.tsv > ${i}_all_a.tsv
awk '{print $1;print$2}' ${wkd}/region_list | parallel --max-args=2 -j 40 final_code.sh {1} {2} ${i}_all_a.tsv ${wkd}/new_only_A_merge.tsv $wkd ${i}
done
######################       finish final train_data ###########################
cat ${wkd}/*coding1.csv > positive_data
cat ${wkd}/*coding0.csv > negative_data

