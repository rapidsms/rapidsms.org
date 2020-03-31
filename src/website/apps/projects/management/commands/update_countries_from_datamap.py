import json

from django.core.management.base import BaseCommand

import requests

from website.apps.projects.models import Country


class Command(BaseCommand):

    help = """Updates Country.datamap_id values from the current version of Datamap.js
           https://raw.github.com/markmarkoh/datamaps/master/public/js/app/data/world-countries.json
           """

    def handle_noargs(self, **options):
        req = requests.get("https://raw.github.com/markmarkoh/datamaps/master/public/js/app/data/world-countries.json")
        # convert into something that can be JSON-ified
        json_data = (json.loads(line.strip()) for line in req.content.split(',\n') if line)
        datamap_id_mapping = dict((datum['id'], datum['properties']['name']) for datum in json_data)
        for code, name in datamap_id_mapping.items():
            obj, created = Country.objects.get_or_create(code=code,
                                                         defaults={'name': name}
                                                         )
            if not created and obj.name != name:
                obj.name = name
                obj.save()
