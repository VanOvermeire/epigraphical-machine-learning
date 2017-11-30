# Inscriptions and Machine Learning

## Overview

An experiment with training Machine Learning models using the collection of inscriptions that the
[Epigraphic Database Heidelberg] [1] offers under a Creative Commons Licence.

[1]: http://edh-www.adw.uni-heidelberg.de/home

## Requirements

- [python 3] [2] with pip
- bash (either a unix based system or an emulator in Windows)
- aws account & [aws cli][3] with your account set as the default
- an [S3 bucket] [4] in your account

[2]: https://www.python.org/downloads/
[3]: https://docs.aws.amazon.com/cli/latest/userguide/installing.html
[4]: https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html

## Running the script

Just run 

`./prepare_and_send_to_aws.sh` 

with the name of your S3 bucket and (optionally) a name for your dataset.
 
#### Notes: 
- you can set the `start` and `end` date in the epi_db_reader.py file. Defaults are '100' and '200'
- you can change the names of the csv with inscriptions and sample file in the prepare_and_send_to_aws file
- generating the model is still TODO! Right now this has to happen manually via the AWS console
