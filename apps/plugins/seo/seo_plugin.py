import logging
import time
import importlib
from typing import List, Dict, Any, Type

from django.conf import settings
from apps.plugins.base.registry import registry

from .title import TitlePlugin
from .meta import MetaPlugin
from .seo_scorer import SEOScorer   # 🔥 NEW

logger = logging.getLogger(__name__)


# =========================
# ⚙️ DEFAULT CONFIG
# =========================
DEFAULT_PLUGINS: List[Type] = [
    TitlePlugin,
    MetaPlugin,
    SEOScorer,   # 🔥 ADDED
]

PLUGIN_PHASES = ["pre", "core", "post"]


# =========================
# 🚀 MAIN LOADER
# =========================
def load_seo_plugins(
    reload: bool = False,
    enabled_plugins: List[str] = None,
    register_core: bool = True,
    dynamic_plugins: List[str] = None,
) -> Dict[str, Any]:

    logger.info("🚀 [SEO LOADER v7] Starting...")

    start_time = time.time()

    if reload:
        if hasattr(registry, "clear"):
            registry.clear()
            logger.warning("♻️ Registry cleared")

    loaded, skipped, failed = [], [], []

    # =========================
    # 🔌 STATIC PLUGINS
    # =========================
    for plugin_cls in DEFAULT_PLUGINS:
        _load_plugin(plugin_cls, enabled_plugins, loaded, skipped, failed)

    # =========================
    # 🌐 DYNAMIC PLUGINS
    # =========================
    if dynamic_plugins:
        for path in dynamic_plugins:
            try:
                plugin_cls = _import_from_path(path)
                _load_plugin(plugin_cls, enabled_plugins, loaded, skipped, failed)
            except Exception as e:
                logger.error(f"[DYNAMIC ERROR] {path}: {e}")
                failed.append(path)

    # =========================
    # 🔥 CORE ENGINE
    # =========================
    if register_core:
        _register_core_engine()

    # =========================
    # 🔀 SORT PLUGINS
    # =========================
    _sort_plugins()

    duration = round(time.time() - start_time, 3)

    summary = {
        "loaded": loaded,
        "skipped": skipped,
        "failed": failed,
        "total": len(getattr(registry, "plugins", [])),
        "load_time": duration,
    }

    logger.info(f"✅ [SEO LOADER DONE] {summary}")

    return summary


# =========================
# 🔌 LOAD SINGLE PLUGIN
# =========================
def _load_plugin(plugin_cls, enabled_plugins, loaded, skipped, failed):

    try:
        plugin = plugin_cls()
        name = getattr(plugin, "name", plugin_cls.__name__)

        # ENV disable
        disabled = getattr(settings, "DISABLED_PLUGINS", [])
        if name in disabled:
            skipped.append(name)
            logger.warning(f"[DISABLED] {name}")
            return

        # selective enable
        if enabled_plugins and name not in enabled_plugins:
            skipped.append(name)
            return

        # duplicate check
        if hasattr(registry, "get_plugin") and registry.get_plugin(name):
            skipped.append(name)
            logger.warning(f"[SKIP] {name} already loaded")
            return

        # validation
        if not hasattr(plugin, "run"):
            raise ValueError(f"{name} missing run()")

        # defaults
        plugin.priority = getattr(plugin, "priority", 100)
        plugin.phase = getattr(plugin, "phase", "core")

        registry.register(plugin)
        loaded.append(name)

        logger.info(f"[LOADED] {name} (phase={plugin.phase}, priority={plugin.priority})")

    except Exception as e:
        logger.error(f"[FAILED] {plugin_cls}: {e}")
        failed.append(str(plugin_cls))


# =========================
# 🔀 SORT PLUGINS
# =========================
def _sort_plugins():
    try:
        if not hasattr(registry, "plugins"):
            return

        registry.plugins.sort(
            key=lambda p: (
                PLUGIN_PHASES.index(getattr(p, "phase", "core"))
                if getattr(p, "phase", "core") in PLUGIN_PHASES else 1,
                getattr(p, "priority", 100)
            )
        )

        logger.info("🔀 Plugins sorted by phase + priority")

    except Exception as e:
        logger.error(f"[SORT ERROR] {e}")


# =========================
# 🔥 CORE ENGINE REGISTER
# =========================
def _register_core_engine():

    try:
        if not hasattr(registry, "register_function"):
            logger.warning("⚠️ register_function not found")
            return

        from apps.plugins.seo.engine import run_seo_plugin

        if hasattr(registry, "get_plugin") and registry.get_plugin("seo_engine"):
            logger.warning("[SKIP] seo_engine already exists")
            return

        registry.register_function("seo_engine", run_seo_plugin)

        logger.info("🔥 Core SEO Engine Registered")

    except Exception as e:
        logger.error(f"[SEO ENGINE ERROR] {e}")


# =========================
# 🌐 DYNAMIC IMPORT
# =========================
def _import_from_path(path: str):
    module_path, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


# =========================
# 🔍 STATUS
# =========================
def get_seo_status():

    try:
        plugins = registry.list_plugins() if hasattr(registry, "list_plugins") else []

        return {
            "total_plugins": len(getattr(registry, "plugins", [])),
            "plugins": plugins,
            "phases": PLUGIN_PHASES,
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# =========================
# 🔁 RELOAD
# =========================
def reload_seo_plugins():
    logger.info("♻️ Reloading SEO Plugins...")
    return load_seo_plugins(reload=True)


# =========================
# 🧠 HEALTH CHECK
# =========================
def seo_health_check():

    try:
        plugins = registry.list_plugins() if hasattr(registry, "list_plugins") else []

        return {
            "status": "healthy",
            "plugin_count": len(plugins),
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}