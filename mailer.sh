#!/bin/bash
#export WORKING_DIR before calling this script
cd $WORKING_DIR
source bin/activate
python manage.py send_mail >> cron_mail.log 2>&1
