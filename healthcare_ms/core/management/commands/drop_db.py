import os
import glob
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Deletes all migration files (except __init__.py) and the database file'

    def handle(self, *args, **kwargs):
        app_dir = settings.APP_DIR
        migration_files = glob.glob(os.path.join(app_dir, '**/migrations/*.py'), recursive=True)

        for file_path in migration_files:
            if not file_path.endswith('__init__.py'):
                try:
                    os.remove(file_path)
                    self.stdout.write(self.style.SUCCESS(f'Deleted: {file_path}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error deleting {file_path}: {str(e)}'))

        # Delete db.sqlite3
        base_dir = settings.BASE_DIR
        db_path = os.path.join(base_dir, 'db.sqlite3')
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                self.stdout.write(self.style.SUCCESS('Deleted: db.sqlite3'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error deleting db.sqlite3: {str(e)}'))
        else:
            self.stdout.write(self.style.WARNING('db.sqlite3 not found'))

        self.stdout.write(self.style.SUCCESS('Successfully cleaned up migration files and database'))
