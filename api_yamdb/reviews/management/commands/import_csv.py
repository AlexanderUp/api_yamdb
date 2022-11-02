from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title
import csv
from pathlib import Path

DIR_PATH = Path.cwd()
print(DIR_PATH)
partial_path = Path(DIR_PATH, 'static', 'data', 'example.csv')
MODELS_DICT = {'category': Category,
               'genre': Genre,
               'genre_title': Genre,
               'titles': Title,
               }


class Command(BaseCommand):
    help = u'Импорт из csv файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            type=str,
            help=u'Имя csv файла')

    def handle(self, *args, **kwargs):
        file_key = kwargs['filename']
        file = file_key + '.csv'     
        full_path = Path(partial_path.with_name(file))
        model_name = MODELS_DICT[file_key]

        with open(full_path, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            count = 0
            for row in file_reader:
                if count == 0:
                    first_row = row
                else:
                    keyargs = dict(zip(first_row, row))
                    model_name.objects.create(**keyargs)
                count += 1
