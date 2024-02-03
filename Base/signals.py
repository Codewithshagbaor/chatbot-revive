from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.models import Room

@receiver(post_save, sender=Room)
def notification_created(sender, instance, created, **kwargs):
    print("Signal received!")
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "send_notification",
                "message": instance.title
            }
        )