from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.utils import timezone
from django.utils.html import escape, mark_safe
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import socket
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop.models import Product
import datetime



class Site(models.Model):
    nom = models.CharField(max_length=50)
    def __str__(self):
        return "%s" % self.nom

    class Meta:
        verbose_name = _('Localisation',)
        verbose_name_plural = _('Localisations')


class Profile(models.Model):

    is_administration = 1
    is_directeur = 2
    ROLE_CHOICES = (
        (is_administration, 'Administration'),
        (is_directeur, 'Directeur'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site,null=True, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

   # is_directeur = models.BooleanField(default=False)
    #is_administration = models.BooleanField(default=False)
    #is_employee= models.BooleanField(default=False)
    matricule = models.CharField(null=False,default='12345', max_length=5,validators=[RegexValidator(r'^\d{1,5}$')])

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
class Order(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    updated = models.DateTimeField(auto_now=True,editable=False)
    #paid = models.BooleanField(default=False)
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return 'Commande {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    #def save(self, *args, **kwargs):
    #    addrs = netifaces.ifaddresses('en0')
    #    self.nom_machine = addrs[netifaces.AF_LINK]
    #    super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    STATUS_CHOICES = (
    ('t', 'Traiter'),
    ('e', 'En cours'),
)
    product = models.ForeignKey(Product,
                                related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order,
                              related_name='items',on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,default='e')
    class Meta:
        verbose_name = 'Articles commandé'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


#class datedispo(models.Model):

#    datedebut=models.DateField(unique=True)
#    datefin=models.DateField(unique=True)

#    def getDatedeb(self):
#        return self.datedebut
#    def getDatefin(self):
#        return self.datefin
