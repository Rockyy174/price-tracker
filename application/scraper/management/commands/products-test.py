from django.core.management.base import BaseCommand

from scraper.models import Website, Product
from scraper.utils import fetch_page, get_price


class Command(BaseCommand):
    help = 'Checks if products can be found'

    def add_arguments(self, parser):
        parser.add_argument('product_id', nargs='*', type=int)

    def handle(self, *args, **options):
        id = options.get('product_id', False)

        # if product ID was provided, checks a single product
        if id:
            product = Product.objects.select_related('website').get(id=id[0])
            page = fetch_page(product.url)

            try:
                get_price(page, product.website.path)
                print('Found:', product.name)
            
            except AttributeError:
                print('Not found:', product.name)
        
        # if product ID was NOT provided, checks all products
        else:
            not_found = []

            for website in Website.objects.all():
                path = website.path

                for product in website.product_set.all():
                    page = fetch_page(product.url)

                    try:
                        get_price(page, path)
                    
                    except AttributeError:
                        not_found.append(product.name)
            
            if not_found:
                print('Not found:')
                for product in not_found:
                    print('\t-', product)
            else:
                print('All products were found')