import email
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User,Profile
from todo.models import Task


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()
    def handle(self, *args, **options):
        user=User.objects.create_user(email=self.fake.email(),nickname=self.fake.name(),password="Todo@#123")
        profile=Profile.objects.get(user=user)
        #complete profile
        profile.first_name=self.fake.first_name()
        profile.last_name=self.fake.last_name()
        profile.description =self.fake.paragraph(nb_sentences=3)
        profile.save()
        #Create Task
        for _ in range(0,5):
            title = self.fake.paragraph(nb_sentences=1)

            task = Task.objects.create(
                user=user, title=title, complete=self.fake.pybool())
            task.save()


        
