from django.contrib.gis.db import models

from common.abstract import CommonAbstractModel


class Setting(CommonAbstractModel):

    key = models.CharField(max_length=255, unique=True)
    value = models.TextField(blank=True, null=True)

    @classmethod
    def get(cls, key, default=None):
        setting = cls.objects.filter(key=key).first()
        if setting:
            return setting.value
        return default

    class Meta:
        verbose_name = "impostazione"
        verbose_name_plural = "impostazioni"

    def __str__(self):
        return self.key
