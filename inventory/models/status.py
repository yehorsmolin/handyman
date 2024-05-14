from django.db import models


class Status(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Statuses"
