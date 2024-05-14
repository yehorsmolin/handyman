from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Vendor(models.Model):
    title = models.CharField(max_length=120)
    contact_person = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    staff = models.ManyToManyField('VendorStaff', related_name='vendors', blank=True)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # ActiveRecord
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Vendors"

