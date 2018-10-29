#!/bin/sh
export S3_BUCKET=filedrive-production
cd ~
source /root/.bash_profile
python /root/filedrive-prod/app.py
