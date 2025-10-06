from .models import Event
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


@receiver(m2m_changed, sender=Event.rsvp.through)
def send_activation_email_for_event_participant(sender, instance, action, **kwargs):
    if action == "post_add":
        User_id=kwargs.get('pk_set')
        user=User.objects.get(id=list(User_id)[0])
        print("user id==", user.id)
        print(instance, instance.rsvp.filter(id=user.id))

        event_participants_emails = [user.email for user in instance.rsvp.filter(id=user.id)]

        send_mail(
            subject=f'You have been added to the event: {instance.name}',
            message=f'Hello,\n\nYou have been added as a participant to the event "{instance.name}".\n\nEvent Details:\nname: {instance.name}\nDescription: {instance.description}\nDate: {instance.date}\nLocation: {instance.location}\n\nThank you for being a part of our community!\n\nBest regards,\nEvent Management Team',
            from_email=settings.EMAIL_HOST_USER,  # Add this line
            recipient_list=event_participants_emails,
            fail_silently=False
        )
