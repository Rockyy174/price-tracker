from __future__ import absolute_import
from celery import shared_task
from django_celery_beat.models import PeriodicTask

from .models import Product
from .utils import fetch_page, get_price


@shared_task(name = "create-price")
def create_price(product_id):
    product = Product.objects.select_related('website').get(id=product_id)   
    page = fetch_page(product.url)
    path = product.website.path

    try:
        price = get_price(page, path)
        product.price_set.create(price=price)
    
    except AttributeError:
        task = PeriodicTask.objects.get(name=product.get_task_name())
        task.delete()