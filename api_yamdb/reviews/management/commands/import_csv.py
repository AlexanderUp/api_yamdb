import csv
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre,  # isort:skip  # noqa
                            Review, Title)

User = get_user_model()

DIR_PATH = settings.BASE_DIR

MODELS = {
    "category": Category,
    "comment": Comment,
    "genre": Genre,
    "review": Review,
    "title": Title,
}

TABLES = ["user", "category", "genre", "title",
          "review", "comment", "genre_title"]


class Command(BaseCommand):
    help = u'Импорт из csv файла в базу данных'

    def handle(self, *args, **kwargs):  # noqa

        for table in TABLES:
            path = Path(DIR_PATH, "static", "data", f"{table}.csv")

            if path.stem == "user":
                with path.open() as source:
                    csv_reader = csv.reader(source, delimiter=",")
                    header = None
                    for row in csv_reader:
                        if not header:
                            header = row
                            continue
                        keyargs = dict(zip(header, row))
                        User.objects.create_user(**keyargs)  # type:ignore
                continue

            if path.stem == "genre_title":
                obj_dict = defaultdict(list)
                with path.open() as source:
                    csv_reader = csv.reader(source, delimiter=",")
                    header = None
                    for row in csv_reader:
                        if not header:
                            header = row
                            continue
                        keyargs = dict(zip(header, row))
                        title = Title.objects.get(pk=keyargs.get("title_id"))
                        genre = Genre.objects.get(pk=keyargs.get("genre_id"))
                        obj_dict[title].append(genre)
                for title in obj_dict:
                    title.genre.set(obj_dict[title], clear=True)
                continue

            model = MODELS.get(f"{path.stem}")

            with path.open() as source:
                obj_list = []
                csv_reader = csv.reader(source, delimiter=",")
                header = None
                for row in csv_reader:
                    if not header:
                        header = row
                        continue
                    keyargs = dict(zip(header, row))
                    obj_list.append(model(**keyargs))  # type:ignore
                model.objects.bulk_create(  # type:ignore
                    obj_list, ignore_conflicts=True
                )
