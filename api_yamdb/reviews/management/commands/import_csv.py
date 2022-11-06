from django.core.management.base import BaseCommand
import sqlite3
import csv
from pathlib import Path
import pandas
from django.db.utils import IntegrityError

from reviews.models import User


DIR_PATH = Path.cwd()

TABLES = ['reviews_category', 'reviews_comment', 'reviews_genre_title',
          'reviews_genre', 'reviews_review', 'reviews_title']


class Command(BaseCommand):
    help = u'Импорт из csv файла в базу данных'

    def handle(self, *args, **kwargs):
        # создание пользователей средствами Django ORM
        full_path = Path(DIR_PATH, 'static', 'data', 'user.csv')
        with open(full_path, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            count = 0
            for row in file_reader:
                if count == 0:
                    first_row = row
                else:
                    keyargs = dict(zip(first_row, row))
                    try:
                        User.objects.create_user(**keyargs)
                    except TypeError:
                        raise TypeError(
                            'Поля файла не соответствуют полям таблицы!'
                        )
                    except IntegrityError:
                        raise IntegrityError(
                            'Поля файла не соответствуют полям таблицы!'
                        )
                count += 1

        # наполнение остальных таблиц
        for table_name in TABLES:
            app, file_name = table_name.split('_', 1)
            file = file_name + '.csv'
            full_path = Path(DIR_PATH, 'static', 'data', file)
            conn = sqlite3.connect('db.sqlite3')
            df = pandas.read_csv(full_path)
            df.to_sql(table_name, conn, if_exists='append', index=False)
