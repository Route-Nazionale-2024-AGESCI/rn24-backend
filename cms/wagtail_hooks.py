from wagtail import hooks

from cms.handlers import ReactPageLinkHandler


@hooks.register("register_rich_text_features", order=10)
def override_link_handler(features):
    features.register_link_type(ReactPageLinkHandler)
