from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Response, Picture


def send_mail(from_email, to_email, username, ad_title, responder_username, response_text, ad_pk):
    html_content = render_to_string( 
            'bbs/mail_new_response.html',
            {
                'username': username,
                'ad_title': ad_title,
                'responder_username': responder_username,
                'response_text': response_text,
                'ad_pk': ad_pk,
            }
        )
    subj = f'New response to your ad {ad_title} from {responder_username}'
    msg = EmailMultiAlternatives(
        subject=subj,
        body=subj,
        from_email=from_email,
        to=[to_email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Response)
def new_response_listener(sender, created, instance, **kwargs):
    if not created:
        return
    ad = instance.ad
    user = instance.ad.user
    email = user.email
    if email:
        send_mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email=email,
            username=user.username,
            ad_title=ad.title,
            responder_username=instance.user.username,
            response_text=instance.text,
            ad_pk=ad.pk,
        )
    print('sent', user.email)


@receiver(post_save, sender=Picture)
def save_pic(sender, instance, created, **kwargs):
    if created:
        instance.save()