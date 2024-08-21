from import_export import resources
from import_export.fields import Field

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
