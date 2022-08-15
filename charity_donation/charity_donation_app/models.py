from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(
        max_length=64
    )

    def __str__(self) -> str:
        return f'{self.name}'


class Institution(models.Model):

    FOUNDATION = 'foundation'
    NON_GOV = 'non-gov organization'
    LOCAL_FUND = 'local fundraising'

    TYPE_CHOICES = [
        (FOUNDATION, 'Fundacja'),
        (NON_GOV, 'Organizacja pozarządowa'),
        (LOCAL_FUND, 'Zbiórka lokalna')
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

    def display_all_categories_separated(self):
        return ', '.join(
            [category.name for category in self.categories.all()]
        )

    def __str__(self) -> str:
        return f'{self.get_type_display()} "{self.name}"'


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

    is_taken = models.BooleanField(
        default=False,
        null=True,
    )

    def display_all_categories_separated(self):
        return ', '.join(
            [category.name for category in self.categories.all()]
        )