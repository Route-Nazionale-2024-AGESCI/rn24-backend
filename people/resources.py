from import_export import resources
from import_export.fields import Field

from people.models.person import Person
from people.models.scout_group import ScoutGroup


class ScoutGroupResource(resources.ModelResource):

    people_count = Field(attribute="people_count")
    children_count = Field(attribute="children_count")
    tents_count = Field(attribute="tents_count")

    class Meta:
        model = ScoutGroup
        fields = (
            "name",
            "zone",
            "people_count",
            "children_count",
            "tents_count",
            "region",
            "line__name",
            "line__subdistrict__name",
            "happiness_path",
            "is_arrived",
            "arrived_at",
            "arrival_date",
            "departure_date",
            "has_problems_with_payments",
            "problems_with_payments",
            "notes",
        )


class PersonResource(resources.ModelResource):

    class Meta:
        model = Person
        fields = (
            "id",
            "created_at",
            "updated_at",
            "uuid",
            "deleted_at",
            "agesci_id",
            "user",
            "first_name",
            "last_name",
            "email",
            "phone",
            "scout_group",
            "is_arrived",
            "arrived_at",
            "birth_date",
            "gender",
            "training_level",
            "address",
            "zip_code",
            "city",
            "province",
            "region",
            "identity_document_type",
            "identity_document_number",
            "identity_document_issue_date",
            "identity_document_expiry_date",
            "accessibility_has_wheelchair",
            "accessibility_has_caretaker_not_registered",
            "sleeping_is_sleeping_in_tent",
            "sleeping_requests",
            "sleeping_place",
            "sleeping_requests_2",
            "sleeping_tent_name",
            "food_diet_needed",
            "food_allergies",
            "food_is_vegan",
            "transportation_has_problems_moving_on_foot",
            "transportation_need_transport",
            "health_has_allergies",
            "health_allergies",
            "health_has_movement_disorders",
            "health_movement_disorders",
            "health_has_patologies",
            "health_patologies",
            "is_available_for_extra_service",
            "note",
            "scout_group__name",
            "scout_group__line__name",
            "scout_group__line__subdistrict__district__name",
        )
