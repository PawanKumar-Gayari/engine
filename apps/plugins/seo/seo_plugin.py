import logging
import time
import importlib
from typing import List, Dict, Any, Type

from django.conf import settings
from apps.plugins.base.registry import registry

from .title import TitlePlugin
from .meta import MetaPlugin


logger = logging.getLogger(__name__)


# =========================
# ⚙️ DEFAULT CONFIG
# =========================
DEFAULT_PLUGINS: List[Type] = [
    TitlePlugin,
    MetaPlugin,
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

    logger.info("🚀 [SEO LOADER v4] Starting...")

    start_time = time.time()

    if reload:
        registry.clear()
        logger.warning("♻️ Registry cleared (reload mode)")

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
    # 🔥 CORE ENGINE (SAFE IMPORT)
    # =========================
    if register_core:
        _register_core_engine()

    duration = round(time.time() - start_time, 3)

    summary = {
        "loaded": loaded,
        "skipped": skipped,
        "failed": failed,
        "total": len(registry.plugins),
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

        # 🔥 ENV CONTROL
        disabled = getattr(settings, "DISABLED_PLUGINS", [])
        if name in disabled:
            skipped.append(name)
            logger.warning(f"[ENV DISABLED] {name}")
            return

        # 🔥 selective load
        if enabled_plugins and name not in enabled_plugins:
            skipped.append(name)
            return

        # 🔥 duplicate check
        if registry.get_plugin(name):
            skipped.append(name)
            logger.warning(f"[SKIP] {name} already loaded")
            return

        # 🔥 validation
        if not hasattr(plugin, "run"):
            raise ValueError(f"{name} missing run()")

        registry.register(plugin)
        loaded.append(name)

        logger.info(f"[LOADED] {name}")

    except Exception as e:
        logger.error(f"[FAILED] {plugin_cls}: {e}")
        failed.append(str(plugin_cls))


# =========================
# 🔥 CORE ENGINE REGISTER (FIXED)
# =========================
def _register_core_engine():

    try:
        if not hasattr(registry, "register_function"):
            logger.warning("⚠️ register_function not found")
            return

        # 🔥 lazy import → circular fix
        from apps.plugins.seo.engine import run_seo_plugin

        if registry.get_plugin("seo_engine"):
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

    return {
        "total_plugins": len(registry.plugins),
        "plugins": registry.list_plugins()
        if hasattr(registry, "list_plugins")
        else [],
        "phases": PLUGIN_PHASES,
    }


# =========================
# 🔁 RELOAD
# =========================
def reload_seo_plugins():
    return load_seo_plugins(reload=True)


# =========================
# 🧠 HEALTH CHECK
# =========================
def seo_health_check():

    try:
        plugins = registry.list_plugins()
        return {
            "status": "healthy",
            "plugin_count": len(plugins),
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }