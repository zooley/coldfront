import os

from django.core.management.base import BaseCommand, CommandError

from common.djangoapps.field_of_science.models import FieldOfScience

app_commands_dir = os.path.dirname(__file__)


class Command(BaseCommand):
    help = 'Import field of science data'

    def handle(self, *args, **options):
        file_path = os.path.join(app_commands_dir, 'data', 'field_of_science_data.csv')
        FieldOfScience.objects.all().delete()
        with open(file_path, 'r') as fp:
            for line in fp:
                print(line.strip())
                pk, parent_id, is_selectable, description, fos_nsf_id, fos_nsf_abbrev, directorate_fos_id = line.strip().split('\t')

                fos = FieldOfScience(
                    pk=pk,
                    is_selectable=is_selectable,
                    description=description,
                    fos_nsf_id=fos_nsf_id,
                    fos_nsf_abbrev=fos_nsf_abbrev,
                    directorate_fos_id=directorate_fos_id
                )
                fos.save()
                if parent_id != 'self':
                    parent_fos = FieldOfScience.objects.get(id=parent_id)
                    fos.parent_id=parent_fos
                    fos.save()
