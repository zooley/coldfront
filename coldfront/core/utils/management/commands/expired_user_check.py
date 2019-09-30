import datetime
import pprint

from django.core.management.base import BaseCommand

from coldfront.core.allocation.models import Allocation, AllocationUser
from coldfront.plugins.freeipa.search import LDAPUserSearch


class Command(BaseCommand):

    def handle(self, *args, **options):
        expired_365_days_ago = datetime.datetime.today() - datetime.timedelta(days=365)

        expired_365_days_ago = expired_365_days_ago.date()
        # Find all active users on active allocations
        active_users = sorted(list(set(AllocationUser.objects.filter(allocation__project__status__name__in=[
            'Active', 'New'], allocation__status__name='Active', status__name='Active').values_list('user__username', flat=True))))

        # Find all user in expired allocations
        expired_allocation_users = {}
        for allocation in Allocation.objects.filter(status__name='Expired'):
            for allocationuser in allocation.allocationuser_set.all():
                if allocationuser.user.username in active_users:
                    continue

                if allocationuser.user.username not in expired_allocation_users:
                    expired_allocation_users[allocationuser.user.username] = {
                        'expire_data': allocation.end_date,
                        'allocation_id': allocation.id
                    }
                else:
                    if allocation.end_date > expired_allocation_users[allocationuser.user.username]['expire_data']:
                        expired_allocation_users[allocationuser.user.username] = {
                            'expire_data': allocation.end_date,
                            'allocation_id': allocation.id
                        }

        # Filter users whose latest allocation expiration date GTE 365 days
        users_with_latest_expiration_lte_365_days = {}
        for key in expired_allocation_users.keys():
            if expired_allocation_users[key]['expire_data'] < expired_365_days_ago:
                user_search = LDAPUserSearch(key, 'username_only')
                if user_search.search():
                    users_with_latest_expiration_lte_365_days[key] = expired_allocation_users[key]
                    print(key)
        users_with_latest_expiration_lte_365_days = dict(
            sorted(users_with_latest_expiration_lte_365_days.items()))
        pprint.pprint(users_with_latest_expiration_lte_365_days)
        print(f'There are {len(users_with_latest_expiration_lte_365_days)} users with expired allocations over 365 days with active status in FreeIPA')
