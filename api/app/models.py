from django.db import models as m

from django.contrib.auth.models import User

class Profil(m.Model):
    user = m.OneToOneField(User , blank=True , null=True , on_delete=m.CASCADE)
    is_chef = m.BooleanField(default=False)
    #img = m.ImageField(null=True ,blank=True)
    def __str__(self):
        return "Profil : " + self.user.username


class Post(m.Model):
    user = m.ForeignKey(User , blank=True , null=True , on_delete=m.CASCADE)
    title = m.CharField(blank=True, null=True,max_length=255)
    description = m.CharField(blank=True, null=True,max_length=2000)
    #img = m.ImageField(blank=True, null=True)
    price = m.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title