from csv import DictReader

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load csv data into Ingredient model from ingredients.csv'

    # def hadle(self, *args, **options):
    #     if Ingredient.objects.exists():
    #         print('ingredients data already loaded...exiting.')
    #         return
    #     print('Loading ingredients data')

    #     for row in DictReader(open(''))
