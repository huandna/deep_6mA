export PATH=/home/yaoxinw/deep_learning/pacbio/software:$PATH
bac=$1
wkd=/home/yaoxinw/deep_learning/pacbio/all_bacteria/${bac}
ref=/home/yaoxinw/bacteria/ref_assembly/${bac}/${bac}_pb.fasta
cd ${wkd}
#######################       prepare_ipdratio_data         ###########################
zcat ${wkd}/modifications.gff.gz | grep -v "##" - | sed 's/ /\t/g' | sed 's/coverage=//' | sed 's/;IPDRatio=/\t/' | sed 's/;context=/\t/' | sed 's/;frac=/\t/' | sed 's/;fracLow=/\t/' | sed 's/;fracUp=/\t/' | sed 's/;identificationQv=/\t/' | sed 's/\t/,/g' > m6A.gff 
zcat ${wkd}/modifications.csv.gz > modifications.csv
merge_modicatoin_gff_csv.py -a ${wkd}/m6A.gff -c ${wkd}/modifications.csv -o only_a.merge.tsv -r $ref
awk '$6!="CC"{print}' only_a.merge.tsv | awk '$6!="GG"{print}' - > new_only_A_merge.tsv



