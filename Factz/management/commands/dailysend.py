from django.core.management.base import BaseCommand

from Factz.dailysend import dailysend

class Command(BaseCommand):
    args = None

    def handle(self, *args, **options):
        val = dailysend()
        return(val)