from django.core.management.base import BaseCommand

from Factz.dailyemail import dailyemail

class Command(BaseCommand):
    args = None

    def handle(self, *args, **options):
        val = dailyemail()
        return(val)