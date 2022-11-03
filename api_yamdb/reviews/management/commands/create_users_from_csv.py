from django.core.management.base import BaseCommand
from users.models import User
import csv
from pathlib import Path
from django.db.utils import IntegrityError

DIR_PATH = Path.cwd()


class Command(BaseCommand):
    help = u'Импорт пользователей из csv файла в базу данных'

    def handle(self, *args, **kwargs):
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
