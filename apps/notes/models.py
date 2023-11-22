from django.db import models

# Create your models here.
class NoteManagement(models.Model):
    title       = models.CharField(max_length=256, null=True, blank=True)
    body        = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    