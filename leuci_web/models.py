"""
from django.db import models

# Create your models here.
### These come from the mictosift demo ###
class Destination(models.Model):
    name=models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    description=models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    slug=models.SlugField()
    
class Cruise(models.Model):
    name=models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    description=models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises'
    )
    slug=models.SlugField()
    

class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT
    )

### Classes more likely in Mutein ###
class Gene(models.Model):
    name=models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    description=models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )    
    

class Structure(models.Model):
    name=models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    description=models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    gene=models.ForeignKey(Gene, on_delete=models.CASCADE)   
    
"""