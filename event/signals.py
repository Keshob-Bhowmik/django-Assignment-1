from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.core.mail import send_mail
from event.models import Event
@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='Particepant')
        instance.groups.add(user_group)
        instance.save()

@receiver(m2m_changed, sender=Event.participants.through)
def notify_participant_rsvp(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        new_participant = instance.participants.model.objects.filter(pk__in = pk_set)
        recipient_emails = [user.email for user in new_participant if user.email]
        if recipient_emails:
            send_mail(
                subject=f"RSVP Confirmation for {instance.name}",
                message=f"Hello!\n\nYou have successfully RSVPed for the event: {instance.name}.\n\nDetails:\nDate: {instance.date}\nTime: {instance.time}\nLocation: {instance.location}\n\nThank you for your participation!",
                from_email="kbbhowmikmontu@gmail.com",
                recipient_list=recipient_emails,
                fail_silently=False,
            )