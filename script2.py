# import os

# import django
# from django.db.models import Q

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coldfront.config.settings")
# django.setup()

# from coldfront.core.allocation.models import Allocation, AllocationAttribute, AllocationAttributeType


# attribute_type_obj = AllocationAttributeType.objects.get(name='slurm_specs')

# resource_name='UB-HPC'

# for allocation in Allocation.objects.filter(
#         status__name='Active',
#         project__status__name__in=['Active', 'New'], resources__name=resource_name):

#     if not allocation.allocationattribute_set.filter(Q(allocation_attribute_type__name='slurm_specs') and Q(value__startswith='Fairshare=100')):
#         AllocationAttribute.objects.create(
#             allocation=allocation,
#             allocation_attribute_type=attribute_type_obj,
#             value='Fairshare=100'
#         )


import os

import django
from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coldfront.config.settings")
django.setup()

from coldfront.core.allocation.models import Allocation, AllocationAttribute, AllocationAttributeType


attribute_type_obj = AllocationAttributeType.objects.get(name='slurm_specs')

resource_name='UB-HPC'

for allocation in Allocation.objects.filter(
        status__name='Active',
        project__status__name__in=['Active', 'New'], resources__name=resource_name):


    fairshare_value = allocation.allocationattribute_set.filter(Q(allocation_attribute_type__name='slurm_specs') and Q(value='Fairshare=100'))
    if fairshare_value and fairshare_value.count() == 1:
        fairshare_value.first().delete()
    elif fairshare_value and fairshare_value.count() > 1:
        print('This should never happen!')
        print(allocation, allocation.id)


