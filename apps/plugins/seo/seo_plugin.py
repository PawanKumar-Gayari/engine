from apps.plugins.base.registry import registry
from .title import TitlePlugin
from .meta import MetaPlugin


def load_seo_plugins():
    registry.register(TitlePlugin())
    registry.register(MetaPlugin())