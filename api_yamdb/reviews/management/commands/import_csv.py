from django.core.management.base import BaseCommand
import sqlite3
from pathlib import Path
import pandas
from reviews.exeptions import FileNameError

DIR_PATH = Path.cwd()

ALLOWED_FILES = ['category', 'comment', 'genre_title',
                 'genre', 'review', 'title']


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
        if file_name not in ALLOWED_FILES:
            raise FileNameError('В базе данных отсутсвует указанная таблица')
        file = file_name + '.csv'
        full_path = Path(DIR_PATH, 'static', 'data', file)
        conn = sqlite3.connect('db.sqlite3')
        df = pandas.read_csv(full_path)
        df.to_sql(table_name, conn, if_exists='append', index=False)
