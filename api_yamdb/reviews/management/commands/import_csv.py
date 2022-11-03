from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title
import sqlite3
from pathlib import Path
from django.db.utils import IntegrityError
import pandas

DIR_PATH = Path.cwd()

MODELS_DICT = {'category': Category,
               'genre': Genre,
               'titles': Title,
               }


class Command(BaseCommand):
    help = u'Импорт из csv файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            'tablename',
            type=str,
            help=u'Название таблицы')

    def handle(self, *args, **kwargs):
        table_name = kwargs['tablename']
        app, file_name = table_name.split('_', 1)
        file = file_name + '.csv'
        full_path = Path(DIR_PATH, 'static', 'data', file)
        conn = sqlite3.connect('db.sqlite3')
        df = pandas.read_csv(full_path)
        df.to_sql(table_name, conn, if_exists='append', index=False)
