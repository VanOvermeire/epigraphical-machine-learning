# Inscriptions and Machine Learning

## Overview

An experiment with training Machine Learning models using the collection of inscriptions that the
[Epigraphic Database Heidelberg] [1] offers under a Creative Commons Licence, plus the power of AWS Machine Learning.

See the article I wrote on this use case [here][2]

[1]: http://edh-www.adw.uni-heidelberg.de/home
[2]: https://www.linkedin.com/pulse/analyzing-roman-inscriptions-aws-machine-learning-sam-van-overmeire/

## Requirements

- [python 3] [3] with pip installer
- the python 'requests' module (`pip3 install requests`)
- bash shell
- aws account
- [aws cli][4] with your account as the default
- an [S3 bucket] [5]

[3]: https://www.python.org/downloads/
[4]: https://docs.aws.amazon.com/cli/latest/userguide/installing.html
[5]: https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html

## Running the script

Download or clone this project. Next, run:

`./prepare_and_send_to_aws.sh` {bucket-here} {optional-name}

with the name of your S3 bucket and (optionally) a name for your dataset. 

The bucket has to allow AWS Machine Learning [access to the objects][6].

[6]: https://docs.aws.amazon.com/machine-learning/latest/dg/granting-amazon-ml-permissions-to-read-your-data-from-amazon-s3.html

#### Notes: 
- you can set the `start` and `end` date in the `epi_db_reader.py` file. Defaults are '100' and '200'
- set the attributes by going to `FIELDS_TO_CHECK` in `epi_db_reader.py`
- you can change the names of the csv with inscriptions and sample file in the `prepare_and_send_to_aws.sh` file
