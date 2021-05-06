export PATH=/home/yaoxinw/deep_learning/pacbio/software:$PATH
bac=$1
wkd=/home/yaoxinw/deep_learning/pacbio/all_bacteria/${bac}
ref=/home/yaoxinw/bacteria/ref_assembly/${bac}/${bac}_pb.fasta
cd ${wkd}
ln -s /home/yaoxinw/bacteria/process/${bac}/all_ipd.bam ${wkd}/all.bam
ln -s /home/yaoxinw/bacteria/process/${bac}/modifications.gff.gz ${wkd}
ln -s /home/yaoxinw/bacteria/process/${bac}/modifications.csv.gz ${wkd}
############################### split_sam ########################################
HEAD_NUMBER=$(samtools view -h ${wkd}/all_ipd.bam | head -n 100 | grep -n -w @PG | tail -n 1 | awk -F ':' '{print $1}')
samtools view -h ${wkd}/all_ipd.bam | head -n $HEAD_NUMBER > ${wkd}/sam_head
samtools view ${wkd}/all.bam > ${wkd}/all_ipd.sam
mkdir -p ${wkd}/split_sam
split -d -n l/100 ${wkd}/all_ipd.sam ${wkd}/split_sam/splitsam
for i in $(ls "$wkd"/split_sam/splitsam*);
do 
cat ${wkd}/sam_head $i > ${i}_new.sam
rm ${i}
done
####################### compute_ipd_&_pw_for_every_base_site###########################
ls ${wkd}/split_sam/*_new.sam | parallel -j 40 --max-args=1 create_IPD_from_sam.py -s {1} -o {1}.tsv
cat ${wkd}/split_sam/*.tsv > ${wkd}/all_a.tsv



