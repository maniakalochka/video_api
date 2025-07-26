from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Запускает кастомный скрипт"

    def handle(self, *args, **options):
        from .gen_fake_data  import generate_test_data

        generate_test_data()
