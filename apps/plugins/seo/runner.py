import logging
from typing import Dict, Any

from apps.plugins.base.registry import registry

logger = logging.getLogger(__name__)


class SEOPluginRunner:
    """
    🔥 Executes all registered SEO plugins in order
    """

    def __init__(self):
        self.registry = registry

    def run(self, content: str, context: Dict[str, Any] = None) -> str:
        context = context or {}

        logger.info("🚀 Starting SEO Plugin Execution")

        if not self.registry.plugins:
            logger.warning("⚠️ No plugins registered")
            return content

        for plugin in self.registry.plugins:

            name = getattr(plugin, "name", plugin.__class__.__name__)

            try:
                logger.info(f"👉 Running plugin: {name}")

                if hasattr(plugin, "run"):
                    content = plugin.run(content, context)

                else:
                    logger.warning(f"⚠️ {name} has no run() method")

            except Exception as e:
                logger.error(f"❌ Plugin failed: {name} → {e}")
                continue  # 🔥 fail-safe (important)

        logger.info("✅ SEO Plugin Execution Complete")

        return content


# 🔥 helper function (easy call)
def apply_seo_plugins(content: str, context: Dict[str, Any] = None) -> str:
    runner = SEOPluginRunner()
    return runner.run(content, context)