class FileNameError(Exception):
    """Ошибка возникает при отсутсвии таблицы в базе данных
    """

    def __init__(self, *args):
        """Преобразование аргумента в сообщение."""
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        """Форматирование сообщения при наличии."""
        if self.message:
            return 'FileNameError, {0}'.format(self.message)
        else:
            'FileNameError has been raised'
