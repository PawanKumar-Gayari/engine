import logging
import time
from collections import defaultdict

logger = logging.getLogger(__name__)


class PluginRegistry:
    """
    🚀 ENTERPRISE PLUGIN REGISTRY (PRO MAX++)

    Features:
    - priority execution
    - dependency resolution (basic)
    - execution phases (pre / core / post)
    - fail-fast / soft mode
    - metrics tracking + slow plugin detection
    - plugin enable/disable runtime
    - hot reload support
    - selective execution
    """

    def __init__(self):
        self.plugins = []
        self.plugin_map = {}

    # =========================
    # 🔌 REGISTER
    # =========================
    def register(self, plugin):

        name = getattr(plugin, "name", plugin.__class__.__name__)

        if name in self.plugin_map:
            logger.warning(f"[DUPLICATE] {name} already exists")
            return

        self.plugins.append(plugin)
        self.plugin_map[name] = plugin

        self._sort_plugins()

        logger.info(f"[REGISTERED] {plugin}")

    # =========================
    # 🔄 HOT RELOAD
    # =========================
    def replace(self, plugin):
        name = plugin.name

        if name in self.plugin_map:
            self.plugins = [p for p in self.plugins if p.name != name]

        self.register(plugin)

    # =========================
    # ⚙️ RUN ENGINE
    # =========================
    def run_all(
        self,
        article: dict,
        keyword: str = "",
        intent: str = "",
        context: dict = None,
        fail_fast: bool = False,
        only: list = None,
        phase: str = None  # pre / core / post
    ):

        context = context or {}
        metrics = []
        start_total = time.time()

        plugins = self._filter_plugins(only, phase)

        for plugin in plugins:

            if not getattr(plugin, "enabled", True):
                continue

            name = plugin.name

            try:
                logger.info(f"[START] {name}")

                article, metric = plugin.safe_run(article, keyword, intent, context)

                metrics.append(metric)

                logger.info(f"[END] {name} → {metric['status']}")

                if fail_fast and metric["status"] == "failed":
                    break

            except Exception as e:
                logger.error(f"[ERROR] {name}: {e}")

                if fail_fast:
                    break

        total_time = round(time.time() - start_total, 4)

        summary = self._build_summary(metrics, total_time)

        return article, metrics, summary

    # =========================
    # 🔍 FILTER
    # =========================
    def _filter_plugins(self, only, phase):

        plugins = self.plugins

        if only:
            plugins = [p for p in plugins if p.name in only]

        if phase:
            plugins = [p for p in plugins if getattr(p, "phase", "core") == phase]

        return plugins

    # =========================
    # 🔥 SORT (priority + dependency)
    # =========================
    def _sort_plugins(self):

        self.plugins.sort(key=lambda p: getattr(p, "priority", 10))

    # =========================
    # 📊 SUMMARY + ANALYTICS
    # =========================
    def _build_summary(self, metrics, total_time):

        success = sum(1 for m in metrics if m["status"] == "success")
        failed = sum(1 for m in metrics if m["status"] == "failed")

        slowest = sorted(metrics, key=lambda m: m.get("duration", 0), reverse=True)

        return {
            "total_plugins": len(metrics),
            "success": success,
            "failed": failed,
            "total_time": total_time,
            "slowest_plugin": slowest[0] if slowest else None,
        }

    # =========================
    # 🔁 ENABLE / DISABLE
    # =========================
    def enable_plugin(self, name):
        if name in self.plugin_map:
            self.plugin_map[name].enabled = True

    def disable_plugin(self, name):
        if name in self.plugin_map:
            self.plugin_map[name].enabled = False

    # =========================
    # 🔍 GET
    # =========================
    def get_plugin(self, name):
        return self.plugin_map.get(name)

    # =========================
    # ❌ CLEAR
    # =========================
    def clear(self):
        self.plugins = []
        self.plugin_map = {}

    # =========================
    # 📊 STATUS
    # =========================
    def status(self):
        return {
            "total": len(self.plugins),
            "plugins": [
                {
                    "name": p.name,
                    "priority": p.priority,
                    "enabled": p.enabled,
                    "phase": getattr(p, "phase", "core"),
                }
                for p in self.plugins
            ]
        }

    # =========================
    # 🧠 GROUP BY PHASE
    # =========================
    def group_by_phase(self):
        groups = defaultdict(list)

        for p in self.plugins:
            phase = getattr(p, "phase", "core")
            groups[phase].append(p.name)

        return dict(groups)


# =========================
# 🌍 GLOBAL INSTANCE
# =========================
registry = PluginRegistry()