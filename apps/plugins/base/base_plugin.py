class BasePlugin:

    name = "base"

    def apply(self, article: dict) -> dict:
        raise NotImplementedError("Plugin must implement apply()")