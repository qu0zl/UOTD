#!/bin/bash
#export WORKING_DIR before calling this script
cd $WORKING_DIR
source bin/activate
python manage.py retry_deferred >> cron_mail_deferred.log 2>&1
