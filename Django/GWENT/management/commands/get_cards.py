from django.core.management.base import BaseCommand, CommandError
from ._cards import get_cards


class Command(BaseCommand):
    help = 'Fill Database with cards'

    def handle(self, *args, **options):
        get_cards()
        self.stdout.write(self.style.SUCCESS("Database full of cards"))