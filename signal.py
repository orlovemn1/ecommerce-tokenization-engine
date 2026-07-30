from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
@receiver(post_save, sender=Order)
def create_token_on_order_save(sender, instance, created,**kwargs):
    if created:
        instance.save_token_to_file()