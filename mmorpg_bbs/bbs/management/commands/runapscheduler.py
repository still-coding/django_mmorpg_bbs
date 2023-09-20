import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from bbs.models import Ad
from user_profiles.models import Profile

logger = logging.getLogger(__name__)


def send_mail(from_email, to_email, mailing_period, username, ads):
    html_content = render_to_string( 
            'bbs/mail_new_ads.html',
            {
                'username': username,
                'mailing_period': mailing_period,
                'ads': ads,
            }
        )

    subj = f'New ads for {mailing_period} day(s)'
    msg = EmailMultiAlternatives(
        subject=subj,
        body=subj,
        from_email=from_email,
        to=[to_email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


 
def send_mail_job():
    print('sending mail')
    profiles = Profile.objects.all()
    for p in profiles:
        if p.mailing_period > 0:
            ads = Ad.objects.filter(created__gte=timezone.now().date() - timedelta(days=p.mailing_period))
            if p.user.email and ads:
                send_mail(
                    mailing_period=p.mailing_period,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_email=p.user.email,
                    username=p.user.username,
                    ads=ads,
                )
                print('sent', p.user.email)


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            send_mail_job,
            trigger=CronTrigger(hour="*/1"),
            id="send_mail_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added daily job 'send_mail_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00",
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
