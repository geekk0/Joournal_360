from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponseRedirect
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys

from journal.views import publish_notes_to_records, update_record_from_note, finalize_note


def publisher():

    ...
    # get accounts, expire them, etc.
    ...
    publish_notes_to_records()


def updater():

    update_record_from_note()


def finalizer():

    finalize_note()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    start_publisher = datetime.strptime('Sep 08 2022  5:28PM', '%b %d %Y %I:%M%p')
    start_updater = datetime.strptime('Sep 08 2022  5:29PM', '%b %d %Y %I:%M%p')
    start_finalizer = datetime.strptime('Sep 08 2022  5:30PM', '%b %d %Y %I:%M%p')

    scheduler.add_job(publisher, 'interval', minutes=50, start_date=start_publisher, name='publish note',
                      jobstore='default')
    scheduler.add_job(updater, 'interval', minutes=50, start_date=start_updater, name='update record',
                      jobstore='default')
    scheduler.add_job(finalizer, 'interval', minutes=50, start_date=start_finalizer, name='finalize note',
                      jobstore='default')

    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)