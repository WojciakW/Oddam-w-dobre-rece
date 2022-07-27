from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(
        max_length=64
    )


class Institution(models.Model):

    TYPE_CHOICES = [
        ('foundation', 'Fundacja'),
        ('non-gov organization', 'Organizacja pozarządowa'),
        ('local fundraising', 'Zbiórka lokalna')
    ]


    name = models.CharField(
        max_length=64
    )

    description = models.TextField()

    type = models.CharField(
        max_length=32,
        choices=TYPE_CHOICES,
        default='foundation'
    )

    categories = models.ManyToManyField(
        to='Category',
    )


class Donation(models.Model):

    quantity = models.IntegerField()

    categories = models.ManyToManyField(
        to='Category'
    )

    institution = models.ForeignKey(
        to='Institution',
        on_delete=models.CASCADE
    )

    address = models.TextField()

    phone_number = models.IntegerField()

    city = models.CharField(
        max_length=32
    )

    zip_code = models.CharField(
        max_length=16
    )

    pick_up_date = models.DateField()

    pick_up_time = models.TimeField()

    pick_up_comment = models.TextField(
        default=None,
        null=True
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )