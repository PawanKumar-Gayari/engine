class PluginRegistry:

    def __init__(self):
        self.plugins = []

    def register(self, plugin):
        self.plugins.append(plugin)

    def apply_all(self, article):
        for plugin in self.plugins:
            article = plugin.apply(article)
        return article


registry = PluginRegistry()