from django.db import models
from django.utils import timezone


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    multiplier = models.IntegerField(default=-1)
    sequence = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['sequence']

    def save(self, *args, **kwargs):
        """
        On Save update some automagic fields
        """
        self.name = self.name.upper()
        if self.id:
            self.modified_at = timezone.now()
        if self.name == "INCOME":
            self.multiplier = 1

        return super().save(*args, **kwargs)

    def get_ui_state(self):
        return 'ui-state-disabled' if self.multiplier == 1 else ''

    def __str__(self):
        return self.name
