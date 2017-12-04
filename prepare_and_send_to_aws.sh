#!/usr/bin/env bash

set -e

if [ $# -lt 1 ]; then
    echo "usage prepare_and_send_to_aws <s3-bucket> [optional-dataset-name]";
    exit 1;
elif [ $# -gt 1 ]; then
    bucket=$1
    dataname=$2
elif [ $# -eq 1 ]; then
    bucket=$1
    dataname='epidata'
fi

# these values can be changed, as long as they end with .csv
shuffled='shuffled_data.csv'
sample='your_sample.csv'
aws_region='eu-west-1'

echo "Generating the data"
python3 epi_db_reader.py

echo "Shuffling dataset and removing 10 inscriptions as an example for evaluating"
shuf files/epi_data.csv > ${shuffled}
cat ${shuffled} | head -n 10 > ${sample}
sed -i -e 1,10d ${shuffled}

s3_shuffled_csv="s3://${bucket}/${dataname}-${shuffled}"
s3_schema="s3://${bucket}/${dataname}-schema.json"

echo "Uploading to S3" # overwrites files with these names
aws s3 cp ${shuffled} ${s3_shuffled_csv}
aws s3 cp files/schema.json ${s3_schema}

datasource_id="${dataname}-source-id"
datasource_name="${dataname}-source-name"

echo "Creating datasource" # S3 bucket permissions will have to allow ML access
aws machinelearning create-data-source-from-s3 --data-source-id ${datasource_id} --data-source-name ${datasource_name} \
--compute-statistics --region ${aws_region} \
--data-spec DataLocationS3=${s3_shuffled_csv},DataSchemaLocationS3=${s3_schema}

datamodel_id="${dataname}-model-id"
datamodel_name="${dataname}-model-name"

aws machinelearning create-ml-model --ml-model-id ${datamodel_id} --ml-model-name ${datamodel_name} \
--ml-model-type MULTICLASS --training-data-source-id  ${datasource_id} --region ${aws_region}

echo "Cleaning up"
rm ${shuffled}

echo "Done!"
