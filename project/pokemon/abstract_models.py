from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField("Name", max_length=255)
    external_id = models.IntegerField("External id", db_index=True)

    def __str__(self):
        return self.name