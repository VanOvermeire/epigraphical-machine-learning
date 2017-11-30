#!/usr/bin/env bash

if [ $# -lt 1 ]; then
    echo "usage prepare_and_send_to_aws <s3-bucket> [optional-dataset-name]";
    exit 1;
elif [ $# -gt 1 ]; then
    echo "here"
    bucket=$1
    dataname=$2
elif [ $# -eq 1 ]; then
    bucket=$1
    dataname='epidata'
fi

# these values can be changed, as long as they end with .csv
shuffled='shuffled_data.csv'
sample='your_sample.csv'
# aws region
region='eu-west-1'

echo "Generating the data"
#python epi_db_reader ACTIVATE

echo "Shuffling dataset and removing 10 inscriptions as an example for evaluating"
shuf files/epi_data.csv > ${shuffled}
cat ${shuffled} | head -n 10 > ${sample}
sed -i -e 1,10d ${shuffled}

echo "Uploading to S3" # overwrites files with these names
#aws s3 cp ${shuffled} s3://${bucket}/${shuffled}
#aws s3 cp files/schema.json s3://${bucket}/${dataname}-schema.json

echo "Creating datasource" # S3 bucket permissions will have to allow ML access
aws machinelearning create-data-source-from-s3 --data-source-id ${dataname} --data-source-name ${dataname} \
--compute-statistics \
--region ${region} \
--data-spec "{ \"DataRearrangement\": \"{ \\\"splitting\\\": {\\\"percentBegin\\\":0,\\\"percentEnd\\\":70 }}\", \"DataLocationS3\": \"s3://${bucket}/${shuffled}\", \"DataSchemaLocationS3\": \"s3://${bucket}/${dataname}-schema.json\" }"
# my god that data-spec was horrible, should have done this part in python

echo "Cleaning up"
rm ${shuffled}

echo "Done"
