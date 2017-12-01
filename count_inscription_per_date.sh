#!/usr/bin/env bash

# assuming date is our first field in the csv
cat files/epi_data.csv | awk -F"," '{print $1}' | sort | uniq -c
