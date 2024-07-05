from people.models.person import Person


class SensibleData(Person):
    class Meta:
        proxy = True
        verbose_name = "Dati sensibili"
        verbose_name_plural = "Dati sensibili"
