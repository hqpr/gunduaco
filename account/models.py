from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField('name', max_length=32)
    email = models.EmailField()
    is_processed = models.BooleanField('Is active', default=True)

    def __unicode__(self):
        return self.name