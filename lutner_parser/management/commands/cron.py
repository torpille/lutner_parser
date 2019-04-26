from django.core.management.base import BaseCommand, CommandError
import os
from crontab import CronTab

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):
        #init cron
        cron = CronTab(user='lisa')

        #add new cron job
        job = cron.new(command='python /home/lisa/dev//example.py >>/tmp/out.txt 2>&1')

        #job settings
        job.minute.every(1)

        cron.write()