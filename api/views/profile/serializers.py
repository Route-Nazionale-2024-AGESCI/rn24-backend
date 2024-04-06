from common.serializers import UUIDRelatedModelSerializer
from people.models.person import Person


class ProfileSerializer(UUIDRelatedModelSerializer):
    class Meta:
        model = Person
        fields = (
            "uuid",
            "created_at",
            "agesci_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "codice_fiscale",
            "birth_date",
            "address",
            "city",
            "scout_group",
            "squads",
        )
