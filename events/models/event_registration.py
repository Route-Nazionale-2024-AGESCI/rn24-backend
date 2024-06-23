from django.db import models

from common.abstract import CommonAbstractModel, NoSoftDeleteMixin


class PersonEventRegistration(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, verbose_name="persona")
    check_in = models.BooleanField(default=False, verbose_name="check-in")

    class Meta:
        verbose_name = "registrazione evento a persona"
        verbose_name_plural = "registrazione evento a persona"

    def __str__(self):
        return f"{self.event} - {self.person}"


class ScoutGroupEventRegistration(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    scout_group = models.ForeignKey(
        "people.ScoutGroup", on_delete=models.CASCADE, verbose_name="gruppo scout"
    )
    check_in = models.BooleanField(default=False, verbose_name="check-in")

    class Meta:
        verbose_name = "registrazione evento a gruppo scout"
        verbose_name_plural = "registrazione evento a gruppo scout"

    def __str__(self):
        return f"{self.event} - {self.scout_group}"


class LineEventRegistration(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    line = models.ForeignKey("people.Line", on_delete=models.CASCADE, verbose_name="fila")
    check_in = models.BooleanField(default=False, verbose_name="check-in")

    class Meta:
        verbose_name = "registrazione evento a fila"
        verbose_name_plural = "registrazione evento a fila"

    def __str__(self):
        return f"{self.event} - {self.line}"


class SubdistrictEventRegistration(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    subdistrict = models.ForeignKey(
        "people.Subdistrict", on_delete=models.CASCADE, verbose_name="contrada"
    )
    check_in = models.BooleanField(default=False, verbose_name="check-in")

    class Meta:
        verbose_name = "registrazione evento a contrada"
        verbose_name_plural = "registrazione evento a contrada"

    def __str__(self):
        return f"{self.event} - {self.subdistrict}"


class DistrictEventRegistration(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    district = models.ForeignKey(
        "people.District", on_delete=models.CASCADE, verbose_name="sottocampo"
    )
    check_in = models.BooleanField(default=False, verbose_name="check-in")

    class Meta:
        verbose_name = "registrazione evento a sottocampo"
        verbose_name_plural = "registrazione evento a sottocampo"

    def __str__(self):
        return f"{self.event} - {self.district}"


class SquadEventRegistration(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    squad = models.ForeignKey("people.Squad", on_delete=models.CASCADE, verbose_name="pattuglia")
    check_in = models.BooleanField(default=False, verbose_name="check-in")

    class Meta:
        verbose_name = "registrazione evento a pattuglia"
        verbose_name_plural = "registrazione evento a pattuglia"

    def __str__(self):
        return f"{self.event} - {self.squad}"
