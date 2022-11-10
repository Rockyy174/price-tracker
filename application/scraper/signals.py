from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .models import Product


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, *args, **kwargs):
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=instance.interval,
        period=instance.period,
    )

    if not created:
        try:
            PeriodicTask.objects.get(name=instance.get_task_name()).delete()
        except PeriodicTask.DoesNotExist:
            pass

    PeriodicTask.objects.create(
        name=instance.get_task_name(),
        task='create-price',
        interval=interval,
        args=[instance.id],
        start_time=timezone.now(),
    )