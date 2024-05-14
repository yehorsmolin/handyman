from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class VendorStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=120, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    owner = models.ForeignKey("Vendor", on_delete=models.CASCADE)

    def __str__(self):
        return self.contact_person

    class Meta:
        verbose_name_plural = "Vendor's Staff"
