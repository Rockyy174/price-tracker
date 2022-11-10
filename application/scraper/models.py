from django.db import models
from django_celery_beat.models import PERIOD_CHOICES


class Website(models.Model):
    """
    Website on which products are tracked

    Fields:
        name: name of website
        path: JSON object with tag and id, class or attrs of the HTML element where price is located.
            child property can be added for nested tags (as many as needed)
            example: {
                "tag": "div",
                "class": "price-container",
                "child": {
                    "tag": "span",
                    "id": "product-price"
                }
            }
    """

    name = models.CharField(max_length=64)
    path = models.JSONField()

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product to be tracked

    Fields:
        website: foreign key to product's website
        name: name of product
        url: url of product
        interval: time indicating how often the product should be checked for price updates
        period: type of interval (days, hours, minutes, seconds or microseconds)
    """

    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    url = models.URLField(max_length=512)
    interval = models.IntegerField(default=24)
    period = models.CharField(max_length=24, choices=PERIOD_CHOICES)

    def __str__(self):
        return self.name
    
    def get_task_name(self):
        return f'{self.name} {self.id}'


class Price(models.Model):
    """
    Price of a product at a specific moment

    Fields:
        product: foreign key to price's product
        price: product's price
        date: moment when the price was checked
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.price}'