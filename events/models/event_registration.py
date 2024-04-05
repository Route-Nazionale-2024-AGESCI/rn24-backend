from django.db import models

from common.abstract import CommonAbstractModel


class PersonEventRegistration(CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, verbose_name="persona")

    class Meta:
        verbose_name = "registrazione evento a persona"
        verbose_name_plural = "registrazione evento a persona"

    def __str__(self):
        return f"{self.event} - {self.person}"


class ScoutGroupEventRegistration(CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    scout_group = models.ForeignKey(
        "people.ScoutGroup", on_delete=models.CASCADE, verbose_name="gruppo scout"
    )

    class Meta:
        verbose_name = "registrazione evento a gruppo scout"
        verbose_name_plural = "registrazione evento a gruppo scout"

    def __str__(self):
        return f"{self.event} - {self.scout_group}"


class SubdistrictEventRegistration(CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    subdistrict = models.ForeignKey(
        "people.Subdistrict", on_delete=models.CASCADE, verbose_name="contrada"
    )

    class Meta:
        verbose_name = "registrazione evento a contrada"
        verbose_name_plural = "registrazione evento a contrada"

    def __str__(self):
        return f"{self.event} - {self.subdistrict}"


class DistrictEventRegistration(CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    district = models.ForeignKey(
        "people.District", on_delete=models.CASCADE, verbose_name="sottocampo"
    )

    class Meta:
        verbose_name = "registrazione evento a sottocampo"
        verbose_name_plural = "registrazione evento a sottocampo"

    def __str__(self):
        return f"{self.event} - {self.district}"


class SquadEventRegistration(CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    squad = models.ForeignKey("people.Squad", on_delete=models.CASCADE, verbose_name="pattuglia")

    class Meta:
        verbose_name = "registrazione evento a pattuglia"
        verbose_name_plural = "registrazione evento a pattuglia"

    def __str__(self):
        return f"{self.event} - {self.squad}"
