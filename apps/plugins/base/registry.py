import logging
import time
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class PluginRegistry:
    """
    🚀 AI EXECUTION REGISTRY v5 (PRO MAX)

    Features:
    - plugin execution engine
    - function registry (NEW)
    - performance tracking
    - smart skip (AI-like)
    - analytics layer
    """

    PHASE_ORDER = ["pre", "core", "post"]

    def __init__(self):
        self.plugins = []
        self.plugin_map = {}
        self.functions = {}  # 🔥 NEW (fix for your error)

        # 🔥 DATA LAYER
        self.history = defaultdict(lambda: deque(maxlen=50))
        self.stats = defaultdict(lambda: {
            "runs": 0,
            "failures": 0,
            "avg_time": 0
        })

    # =========================
    # 🔌 REGISTER PLUGIN
    # =========================
    def register(self, plugin):

        name = getattr(plugin, "name", plugin.__class__.__name__)

        if name in self.plugin_map:
            return

        plugin.enabled = getattr(plugin, "enabled", True)
        plugin.priority = getattr(plugin, "priority", 10)
        plugin.phase = getattr(plugin, "phase", "core")

        self.plugins.append(plugin)
        self.plugin_map[name] = plugin

        self._sort_plugins()

    # =========================
    # 🔥 REGISTER FUNCTION (NEW)
    # =========================
    def register_function(self, name, func):

        if name in self.functions:
            logger.warning(f"[SKIP] Function {name} already exists")
            return

        self.functions[name] = func
        logger.info(f"[FUNCTION REGISTERED] {name}")

    # =========================
    # 🚀 RUN FUNCTION (NEW)
    # =========================
    def run_function(self, name, *args, **kwargs):

        if name not in self.functions:
            raise ValueError(f"Function '{name}' not found")

        return self.functions[name](*args, **kwargs)

    # =========================
    # 🚀 MAIN EXECUTION
    # =========================
    def run_all(
        self,
        article: dict,
        keyword: str = "",
        intent: str = "",
        context: dict = None,
        fail_fast: bool = False,
        only: list = None,
        phase: str = None
    ):

        context = context or {}
        metrics = []
        start_total = time.time()

        phases = [phase] if phase else self.PHASE_ORDER

        for ph in phases:

            plugins = self._filter_plugins(only, ph)

            for plugin in plugins:

                if not plugin.enabled:
                    continue

                name = plugin.name

                # 🔥 SMART SKIP
                if self._should_skip(name):
                    logger.info(f"[SKIP AI] {name}")
                    continue

                start = time.time()

                try:
                    result = plugin.run(article, keyword, intent, context)
                    article = result if result else article

                    duration = round(time.time() - start, 4)

                    metric = {
                        "plugin": name,
                        "status": "success",
                        "duration": duration
                    }

                    self._update_stats(name, duration, True)

                except Exception as e:
                    duration = round(time.time() - start, 4)

                    metric = {
                        "plugin": name,
                        "status": "failed",
                        "error": str(e),
                        "duration": duration
                    }

                    self._update_stats(name, duration, False)

                    if fail_fast:
                        break

                metrics.append(metric)

        total_time = round(time.time() - start_total, 4)
        summary = self._build_summary(metrics, total_time)

        return article, metrics, summary

    # =========================
    # 🧠 AI SKIP LOGIC
    # =========================
    def _should_skip(self, name):

        stat = self.stats[name]

        if stat["runs"] > 10 and stat["failures"] / stat["runs"] > 0.5:
            return True

        if stat["avg_time"] > 2.0:
            return True

        return False

    # =========================
    # 📊 UPDATE STATS
    # =========================
    def _update_stats(self, name, duration, success):

        stat = self.stats[name]

        stat["runs"] += 1
        stat["avg_time"] = (
            (stat["avg_time"] * (stat["runs"] - 1) + duration) / stat["runs"]
        )

        if not success:
            stat["failures"] += 1

        self.history[name].append({
            "duration": duration,
            "success": success
        })

    # =========================
    # 🔍 FILTER
    # =========================
    def _filter_plugins(self, only, phase):

        plugins = self.plugins

        if only:
            plugins = [p for p in plugins if p.name in only]

        if phase:
            plugins = [p for p in plugins if p.phase == phase]

        return plugins

    # =========================
    # 🔀 SORT
    # =========================
    def _sort_plugins(self):

        self.plugins.sort(
            key=lambda p: (
                self.PHASE_ORDER.index(p.phase) if p.phase in self.PHASE_ORDER else 1,
                getattr(p, "priority", 10),
                self.stats[p.name]["avg_time"]
            )
        )

    # =========================
    # 📊 SUMMARY
    # =========================
    def _build_summary(self, metrics, total_time):

        success = sum(1 for m in metrics if m["status"] == "success")
        failed = sum(1 for m in metrics if m["status"] == "failed")

        return {
            "total_plugins": len(metrics),
            "success": success,
            "failed": failed,
            "total_time": total_time,
        }

    # =========================
    # 📈 ANALYTICS
    # =========================
    def analytics(self):

        return {
            name: {
                "runs": s["runs"],
                "failures": s["failures"],
                "avg_time": round(s["avg_time"], 4)
            }
            for name, s in self.stats.items()
        }

    # =========================
    # 🔍 GET
    # =========================
    def get_plugin(self, name):
        return self.plugin_map.get(name)

    def list_plugins(self):
        return list(self.plugin_map.keys())

    def clear(self):
        self.plugins.clear()
        self.plugin_map.clear()
        self.functions.clear()


# =========================
# 🌍 GLOBAL INSTANCE
# =========================
registry = PluginRegistry()