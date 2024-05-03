from wagtail.rich_text import LinkHandler

from cms.models.page import CMSPage


class ReactPageLinkHandler(LinkHandler):
    identifier = "page"

    @classmethod
    def get_instance(cls, attrs):
        return CMSPage.objects.get(id=attrs["id"])

    @classmethod
    def expand_db_attributes(cls, attrs):
        page = cls.get_instance(attrs)
        return f'<Link to="pages/{page.uuid}">{page.title}</Link>'
