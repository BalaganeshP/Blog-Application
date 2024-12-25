
from typing import Any
from blog.models import category
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help="This commands inserts category data"

    def handle(self, *args:Any, **options:Any):
        #delete existing data
        category.objects.all().delete()

        categories =['Sports','Technology','Science','Art','Food']
      

        for category_name in categories:
           category.objects.create(name=category_name) 
           
            
        self.stdout.write(self.style.SUCCESS("Completed inserting Data!"))
