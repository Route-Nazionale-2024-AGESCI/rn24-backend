from django.contrib.auth import get_user_model
from django.db import models

from common.abstract import CommonAbstractModel

User = get_user_model()


class Person(CommonAbstractModel):

    agesci_id = models.CharField(
        max_length=255, db_index=True, verbose_name="codice AGESCI", unique=True
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="utente")

    first_name = models.CharField(db_index=True, max_length=255, verbose_name="nome")
    last_name = models.CharField(db_index=True, max_length=255, verbose_name="cognome")
    email = models.EmailField(db_index=True, unique=True, verbose_name="email")
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name="telefono")
    codice_fiscale = models.CharField(
        db_index=True,
        max_length=16,
        verbose_name="codice fiscale",
        unique=True,
        null=True,
        blank=True,
    )
    birth_date = models.DateField(verbose_name="data di nascita", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="indirizzo", null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name="città", null=True, blank=True)

    scout_group = models.ForeignKey(
        "people.ScoutGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="gruppo scout",
    )

    squads = models.ManyToManyField(
        "people.Squad", related_name="members", blank=True, verbose_name="pattuglie"
    )

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "persone"

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.scout_group}]"
