from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Add user(s) to the member group'

    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='+', type=str,
                          help='Username(s) to add to member group')

    def handle(self, *args, **options):
        User = get_user_model()
        member_group, created = Group.objects.get_or_create(name='member')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created "member" group.')
            )

        for username in options['usernames']:
            try:
                user = User.objects.get(username=username)
                if user.groups.filter(name='member').exists():
                    self.stdout.write(
                        self.style.WARNING(f'{username} is already a member.')
                    )
                else:
                    user.groups.add(member_group)
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully added {username} to member group.')
                    )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User "{username}" does not exist.')
                )
