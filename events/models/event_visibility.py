from django.db import models

from common.abstract import CommonAbstractModel, NoSoftDeleteMixin


class PersonEventVisibility(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, verbose_name="persona")

    class Meta:
        verbose_name = "disponibilità evento a persona"
        verbose_name_plural = "disponibilità evento a persona"

    def __str__(self):
        return f"{self.event} - {self.person}"


class ScoutGroupEventVisibility(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    scout_group = models.ForeignKey(
        "people.ScoutGroup", on_delete=models.CASCADE, verbose_name="gruppo scout"
    )

    class Meta:
        verbose_name = "disponibilità evento a gruppo scout"
        verbose_name_plural = "disponibilità evento a gruppo scout"

    def __str__(self):
        return f"{self.event} - {self.scout_group}"


class LineEventVisibility(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    line = models.ForeignKey("people.Line", on_delete=models.CASCADE, verbose_name="fila")

    class Meta:
        verbose_name = "disponibilità evento a fila"
        verbose_name_plural = "disponibilità evento a fila"

    def __str__(self):
        return f"{self.event} - {self.line}"


class SubdistrictEventVisibility(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    subdistrict = models.ForeignKey(
        "people.Subdistrict", on_delete=models.CASCADE, verbose_name="contrada"
    )

    class Meta:
        verbose_name = "disponibilità evento a contrada"
        verbose_name_plural = "disponibilità evento a contrada"

    def __str__(self):
        return f"{self.event} - {self.subdistrict}"


class DistrictEventVisibility(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    district = models.ForeignKey(
        "people.District", on_delete=models.CASCADE, verbose_name="sottocampo"
    )

    class Meta:
        verbose_name = "disponibilità evento a sottocampo"
        verbose_name_plural = "disponibilità evento a sottocampo"

    def __str__(self):
        return f"{self.event} - {self.district}"


class SquadEventVisibility(NoSoftDeleteMixin, CommonAbstractModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name="evento")
    squad = models.ForeignKey("people.Squad", on_delete=models.CASCADE, verbose_name="pattuglia")

    class Meta:
        verbose_name = "disponibilità evento a pattuglia"
        verbose_name_plural = "disponibilità evento a pattuglia"

    def __str__(self):
        return f"{self.event} - {self.squad}"
