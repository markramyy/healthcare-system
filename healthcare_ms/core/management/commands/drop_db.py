import os
import glob
import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Deletes all migration files (except __init__.py) and drops/recreates the PostgreSQL database'

    def handle(self, *args, **kwargs):
        # Delete migration files
        app_dir = settings.APP_DIR
        migration_files = glob.glob(os.path.join(app_dir, '**/migrations/*.py'), recursive=True)

        for file_path in migration_files:
            if not file_path.endswith('__init__.py'):
                try:
                    os.remove(file_path)
                    self.stdout.write(self.style.SUCCESS(f'Deleted: {file_path}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error deleting {file_path}: {str(e)}'))

        # Get database settings
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        # Connect to postgres database to drop the target database
        try:
            # Connect to postgres database (not the target database)
            conn = psycopg2.connect(
                dbname='postgres',
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            conn.autocommit = True
            cursor = conn.cursor()

            # Terminate all connections to the target database
            cursor.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{db_name}'
                AND pid <> pg_backend_pid();
            """)

            # Drop and recreate the database
            cursor.execute(f'DROP DATABASE IF EXISTS "{db_name}";')
            self.stdout.write(self.style.SUCCESS(f'Dropped database: {db_name}'))

            cursor.execute(f'CREATE DATABASE "{db_name}";')
            self.stdout.write(self.style.SUCCESS(f'Created database: {db_name}'))

            cursor.close()
            conn.close()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error managing database: {str(e)}'))
            return

        self.stdout.write(self.style.SUCCESS('Successfully cleaned up migration files and database'))
