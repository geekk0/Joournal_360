import socket

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
import sys
from journal.views import logger
from journal.views import publish_eng_record, publish_it_record, update_eng_record, update_it_record, send_eng_email,\
    send_it_email, finalize_eng_note, finalize_it_note


def eng_publisher():

    ...
    # get accounts, expire them, etc.
    ...

    publish_eng_record()


def eng_updater():           #Eng

    update_eng_record()


def eng_email_sender():

    send_eng_email()


def eng_finalizer():

    finalize_eng_note()


def it_publisher():             #IT

    ...
    # get accounts, expire them, etc.
    ...

    publish_it_record()


def it_updater():

    update_it_record()


def it_email_sender():

    send_it_email()


def it_finalizer():

    finalize_it_note()


def start():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47200))
    except socket.error:
        logger.debug("!!!scheduler already started, DO NOTHING")
    else:

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        start_eng_publisher = datetime.strptime('Oct 15 2021  9:10AM', '%b %d %Y %I:%M%p')
        start_eng_updater = datetime.strptime('Oct 15 2021  9:23AM', '%b %d %Y %I:%M%p')
        start_eng_email_sender = datetime.strptime('Oct 15 2021  11:00AM', '%b %d %Y %I:%M%p')
        start_eng_finalizer = datetime.strptime('Oct 15 2021  8:01PM', '%b %d %Y %I:%M%p')

        """start_it_publisher = datetime.strptime('Oct 15 2021  10:30AM', '%b %d %Y %I:%M%p')
        start_it_updater = datetime.strptime('Oct 15 2021  10:43AM', '%b %d %Y %I:%M%p')
        start_it_email_sender = datetime.strptime('Oct 15 2021  10:31AM', '%b %d %Y %I:%M%p')
        start_it_finalizer = datetime.strptime('Oct 15 2021  8:02PM', '%b %d %Y %I:%M%p')"""

        scheduler.add_job(eng_publisher, 'interval', days=1, start_date=start_eng_publisher, id='eng_publisher',
                          jobstore='default', replace_existing=True, max_instances=1, coalesce=True)
        scheduler.add_job(eng_updater, 'interval', minutes=30, start_date=start_eng_updater, id='eng_updater',
                          jobstore='default', replace_existing=True)
        scheduler.add_job(eng_email_sender, 'interval', days=1, start_date=start_eng_email_sender,
                          id='eng_email_sender',
                          jobstore='default', replace_existing=True, max_instances=1, coalesce=True)
        scheduler.add_job(eng_finalizer, 'interval', days=1, start_date=start_eng_finalizer, id='eng_finalizer',
                          jobstore='default', replace_existing=True, max_instances=1)

        """scheduler.add_job(it_publisher, 'interval', days=1, start_date=start_it_publisher, id='it_publisher',
                          jobstore='default', replace_existing=True, max_instances=1, coalesce=True)
        scheduler.add_job(it_email_sender, 'interval', days=1, start_date=start_it_email_sender,
                          id='it_email_sender',
                          jobstore='default', replace_existing=True, max_instances=1, coalesce=True)
        scheduler.add_job(it_updater, 'interval', minutes=30, start_date=start_it_updater, id='it_updater',
                          jobstore='default', replace_existing=True)
        scheduler.add_job(it_finalizer, 'interval', days=1, start_date=start_it_finalizer, id='it_finalizer',
                          jobstore='default', replace_existing=True, max_instances=1)"""

        scheduler.start()
        print("Scheduler started...", file=sys.stdout)