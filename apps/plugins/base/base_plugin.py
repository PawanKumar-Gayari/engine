import time
import traceback
import logging
from copy import deepcopy
from collections import deque


logger = logging.getLogger(__name__)


class BasePlugin:
    """
    🚀 AI CORE PLUGIN v4 (DATA + LEARNING ENGINE)

    NEW:
    - performance DB (in-memory)
    - learning memory
    - adaptive optimization
    """

    name = "base"
    version = "3.0"
    priority = 10
    enabled = True
    phase = "core"

    # 🔥 execution control
    max_retries = 1
    timeout = 5
    fail_silently = True

    config = {}

    # =========================
    # 🧠 DATA LAYER (NEW)
    # =========================
    performance_db = {
        "runs": 0,
        "failures": 0,
        "avg_time": 0
    }

    history = deque(maxlen=50)  # last 50 runs

    # =========================
    # 🚀 MAIN ENTRY
    # =========================
    def run(self, article: dict, keyword: str = "", intent: str = "", context: dict = None) -> dict:
        return self.apply(article)

    def apply(self, article: dict) -> dict:
        raise NotImplementedError

    # =========================
    # 🧠 EXECUTION DECISION
    # =========================
    def should_run(self, article, keyword, intent, context):

        # 🔥 skip if too many failures
        if self.performance_db["runs"] > 10:
            fail_rate = self.performance_db["failures"] / self.performance_db["runs"]
            if fail_rate > 0.5:
                return False

        return True

    # =========================
    # 🛡️ SAFE EXECUTION
    # =========================
    def safe_run(self, article, keyword="", intent="", context=None):

        context = context or {}

        if not self.enabled:
            return article, self._metric("skipped_disabled")

        if not self.should_run(article, keyword, intent, context):
            return article, self._metric("skipped_ai")

        attempt = 0
        last_error = None

        while attempt <= self._adaptive_retries():

            attempt += 1
            start = time.time()

            try:
                safe_article = deepcopy(article)

                result = self.before_run(safe_article, keyword, intent, context)
                result = self.run(result, keyword, intent, context)
                result = self.validate(result)
                result = self.after_run(result, keyword, intent, context)

                duration = round(time.time() - start, 4)

                # 🔥 update DATA LAYER
                self._update_stats(duration, success=True)

                return result, self._metric("success", duration, attempt)

            except Exception as e:
                last_error = e

                duration = round(time.time() - start, 4)

                self._update_stats(duration, success=False)

                self._log_error(e, attempt)

                if attempt > self._adaptive_retries():
                    break

        if not self.fail_silently:
            raise last_error

        return article, self._metric("failed", error=str(last_error), attempt=attempt)

    # =========================
    # 🔁 ADAPTIVE RETRIES
    # =========================
    def _adaptive_retries(self):

        # 🔥 increase retries if success rate high
        runs = self.performance_db["runs"]

        if runs > 10:
            fail_rate = self.performance_db["failures"] / runs
            if fail_rate < 0.2:
                return self.max_retries + 1

        return self.max_retries

    # =========================
    # 📊 DATA UPDATE
    # =========================
    def _update_stats(self, duration, success):

        db = self.performance_db

        db["runs"] += 1

        # avg time update
        db["avg_time"] = (
            (db["avg_time"] * (db["runs"] - 1) + duration) / db["runs"]
        )

        if not success:
            db["failures"] += 1

        # 🔥 history store
        self.history.append({
            "duration": duration,
            "success": success
        })

    # =========================
    # 🧠 HOOKS
    # =========================
    def before_run(self, article, keyword, intent, context):
        return article

    def after_run(self, article, keyword, intent, context):
        return article

    # =========================
    # ✅ VALIDATION
    # =========================
    def validate(self, article):

        if not isinstance(article, dict):
            raise ValueError(f"{self.name}: output must be dict")

        if "content" not in article:
            article["content"] = article.get("content", "")

        return article

    # =========================
    # 📊 METRICS
    # =========================
    def _metric(self, status, duration=0, attempt=1, error=None):
        return {
            "plugin": self.name,
            "status": status,
            "duration": duration,
            "attempt": attempt,
            "error": error,
            "performance": self.performance_db
        }

    # =========================
    # 📊 LOGGING
    # =========================
    def _log_error(self, error, attempt):
        logger.error(f"[ERROR] {self.name} | attempt={attempt} | {error}")
        traceback.print_exc()

    # =========================
    # 📈 ANALYTICS (NEW)
    # =========================
    def analytics(self):
        return {
            "performance": self.performance_db,
            "history": list(self.history)
        }

    # =========================
    # ⚙️ CONFIG
    # =========================
    def get_config(self, key, default=None):
        return self.config.get(key, default)

    def __repr__(self):
        return f"<Plugin {self.name} v{self.version}>"