from django.db import models
from accounts.models import User

# Create your models here.


class VerificationContent(models.Model):
    content = models.CharField(
        verbose_name='Verification Content',
        max_length=20,
        blank=False,
        null=False,
    )
    lic_feature_base_a = models.BooleanField(
        verbose_name='License Feature Base_A',
    )
    lic_feature_base_b = models.BooleanField(
        verbose_name='License Feature Base_B',
    )
    lic_feature_base_c = models.BooleanField(
        verbose_name='License Feature Base_C',
    )
    lic_feature_opt_1 = models.BooleanField(
        verbose_name='License Feature Option_1',
    )
    lic_feature_opt_2 = models.BooleanField(
        verbose_name='License Feature Option_2',
    )
    lic_feature_opt_3 = models.BooleanField(
        verbose_name='License Feature Option_3',
    )
    user_create = models.ForeignKey(
        User,
        verbose_name='User(Create)',
        blank=True,
        null=True,
        related_name='ContentUserCreate',
        on_delete=models.SET_NULL,
        editable=False,
    )
    time_create = models.DateTimeField(
        verbose_name='Time(Create)',
        blank=True,
        null=True,
        editable=False,
    )
    user_update = models.ForeignKey(
        User,
        verbose_name='User(Update)',
        blank=True,
        null=True,
        related_name='ContentUserUpdate',
        on_delete=models.SET_NULL,
        editable=False,
    )
    time_update = models.DateTimeField(
        verbose_name='Time(Update)',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        return self.content


class Technology(models.Model):
    tech_node = models.CharField(
        verbose_name='Technology Node',
        max_length=20,
        blank=False,
        null=False,
    )

    lic_16nm = models.BooleanField(
        verbose_name='16nm',
    )

    peak_lic_7nm = models.BooleanField(
        verbose_name='7nm',
    )
    user_create = models.ForeignKey(
        User,
        verbose_name='User(Create)',
        blank=True,
        null=True,
        related_name='TechUserCreate',
        on_delete=models.SET_NULL,
        editable=False,
    )
    time_create = models.DateTimeField(
        verbose_name='Time(Create)',
        blank=True,
        null=True,
        editable=False,
    )
    user_update = models.ForeignKey(
        User,
        verbose_name='User(Update)',
        blank=True,
        null=True,
        related_name='TechUserUpdate',
        on_delete=models.SET_NULL,
        editable=False,
    )
    time_update = models.DateTimeField(
        verbose_name='Time(Update)',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        return self.tech_node


class Demand(models.Model):
    product = models.CharField(
        verbose_name='Product Name(Design Phase)',
        max_length=20,
        blank=False,
        null=False,
    )
    technology = models.ForeignKey(
        Technology,
        verbose_name='Technology',
        blank=False,
        null=True,
        related_name='technology',
        on_delete=models.SET_NULL,
    )
    content = models.ForeignKey(
        VerificationContent,
        verbose_name='Verification Content',
        blank=False,
        null=True,
        related_name='VerificationContent',
        on_delete=models.SET_NULL,
    )

    start_date = models.DateField(
        verbose_name='Start Date',
        blank=False,
        null=False,
    )
    end_date = models.DateField(
        verbose_name='End Date',
        blank=False,
        null=False,
    )

    frequency = models.IntegerField(
        verbose_name='Frequency of Use [%]',
        blank=False,
        null=False,
    )
    comment = models.TextField(
        verbose_name='Comments',
        blank=True,
        null=True,
    )
    user_create = models.ForeignKey(
        User,
        verbose_name='User(Create)',
        blank=True,
        null=True,
        related_name='DemandUserCreate',
        on_delete=models.SET_NULL,
        editable=False,
    )
    time_create = models.DateTimeField(
        verbose_name='Time(Create)',
        blank=True,
        null=True,
        editable=False,
    )
    user_update = models.ForeignKey(
        User,
        verbose_name='User(Update)',
        blank=True,
        null=True,
        related_name='DemandUserUpdate',
        on_delete=models.SET_NULL,
        editable=False,
    )
    time_update = models.DateTimeField(
        verbose_name='Time(Update)',
        blank=True,
        null=True,
        editable=False,
    )
    def __str__(self):
        return self.product
