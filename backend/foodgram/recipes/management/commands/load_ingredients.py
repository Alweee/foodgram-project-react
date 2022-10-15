import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load csv data into Ingredient model from ingredients.csv file.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r', encoding='UTF-8') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            for row in data:
                Ingredient.objects.get_or_create(
                    name=row[0], measurement_unit=row[1])

        self.stdout.write(self.style.SUCCESS('Data uploaded successfully'))
