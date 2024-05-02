import pytest
from django.urls import reverse
from rest_framework.fields import DateTimeField

from cms.factories import CMSPageFactory


@pytest.mark.django_db
def test_get_pages(logged_api_client, root_page):
    url = reverse("page-list")
    page = CMSPageFactory(parent=root_page)
    page.save_revision().publish()
    response = logged_api_client.get(url)
    assert response.status_code == 200
    assert response.json() == [
        {
            "uuid": str(root_page.uuid),
            "created_at": DateTimeField().to_representation(root_page.created_at),
            "title": root_page.title,
            "slug": root_page.slug,
            "show_in_menus": root_page.show_in_menus,
            "body": root_page.serve(request=response.wsgi_request).render().content.decode("utf-8"),
            "parent_link": "",
            "parent": None,
            "children_link": [f'<Link to="pages/{page.uuid}">'],
            "children": [
                {
                    "uuid": str(page.uuid),
                    "created_at": DateTimeField().to_representation(page.created_at),
                    "title": page.title,
                    "slug": page.slug,
                    "show_in_menus": page.show_in_menus,
                    "body": page.serve(request=response.wsgi_request)
                    .render()
                    .content.decode("utf-8"),
                    "parent": str(root_page.uuid),
                    "parent_link": f'<Link to="pages/{root_page.uuid}">',
                    "children_link": [],
                    "children": [],
                },
            ],
        }
    ]
