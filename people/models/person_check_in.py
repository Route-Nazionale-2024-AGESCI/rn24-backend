from django.contrib.auth import get_user_model
from django.db import models

from common.abstract import CommonAbstractModel
from people.models.person import Person

User = get_user_model()


class PersonCheckIn(CommonAbstractModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    direction = models.CharField(
        max_length=255,
        choices=(
            ("ENTRATA", "ENTRATA"),
            ("USCITA", "USCITA"),
        ),
        db_index=True,
        verbose_name="direzione",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="utente")

    class Meta:
        verbose_name = "entrata - uscita"
        verbose_name_plural = "entrate - uscite"
