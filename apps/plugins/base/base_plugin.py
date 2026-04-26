import time
import traceback
import logging
from copy import deepcopy


logger = logging.getLogger(__name__)


class BasePlugin:
    """
    🚀 ULTRA NEXT-LEVEL PLUGIN CORE (Enterprise + SaaS Ready)

    Features:
    - priority + enable control
    - retries + timeout protection
    - safe execution (no crash)
    - structured metrics + lifecycle tracking
    - shared context (mutable safely)
    - validation layer
    - pre/post hooks
    - soft-fail / hard-fail modes
    - plugin versioning
    """

    name = "base"
    version = "1.0"
    priority = 10
    enabled = True

    # 🔥 execution control
    max_retries = 1
    timeout = 5  # seconds (soft limit)

    # 🔥 failure mode
    fail_silently = True

    # 🔥 optional config
    config = {}

    # =========================
    # 🚀 MAIN ENTRY
    # =========================
    def run(self, article: dict, keyword: str = "", intent: str = "", context: dict = None) -> dict:
        return self.apply(article)

    def apply(self, article: dict) -> dict:
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement run() or apply()"
        )

    # =========================
    # 🛑 SHOULD RUN
    # =========================
    def should_run(self, article, keyword, intent, context):
        return True

    # =========================
    # 🛡️ SAFE EXECUTION CORE
    # =========================
    def safe_run(self, article: dict, keyword: str = "", intent: str = "", context: dict = None):

        context = context or {}

        if not self.enabled:
            return article, self._metric("skipped_disabled")

        if not self.should_run(article, keyword, intent, context):
            return article, self._metric("skipped_condition")

        attempt = 0
        last_error = None

        while attempt <= self.max_retries:

            attempt += 1
            start = time.time()

            try:
                # 🔹 deep copy for safety
                safe_article = deepcopy(article)

                # 🔹 before hook
                safe_article = self.before_run(safe_article, keyword, intent, context)

                # 🔹 main execution
                result = self.run(safe_article, keyword, intent, context)

                # 🔹 validation
                result = self.validate(result)

                # 🔹 after hook
                result = self.after_run(result, keyword, intent, context)

                duration = round(time.time() - start, 4)

                # 🔹 timeout check (soft)
                if duration > self.timeout:
                    logger.warning(f"[PLUGIN TIMEOUT] {self.name} took {duration}s")

                self._log_success(duration, attempt)

                return result, self._metric("success", duration, attempt)

            except Exception as e:
                last_error = e
                self._log_error(e, attempt)

                if attempt > self.max_retries:
                    break

        # =========================
        # ❌ FINAL FAILURE
        # =========================
        if not self.fail_silently:
            raise last_error

        return article, self._metric("failed", error=str(last_error), attempt=attempt)

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
            raise ValueError(f"{self.name}: missing 'content'")

        return article

    # =========================
    # 📊 METRICS SYSTEM
    # =========================
    def _metric(self, status, duration=0, attempt=1, error=None):
        return {
            "plugin": self.name,
            "version": self.version,
            "status": status,
            "duration": duration,
            "attempt": attempt,
            "error": error,
        }

    # =========================
    # 📊 LOGGING
    # =========================
    def _log_success(self, duration, attempt):
        logger.info(
            f"[PLUGIN SUCCESS] {self.name} v{self.version} | "
            f"{duration}s | attempt={attempt}"
        )

    def _log_error(self, error, attempt):
        logger.error(
            f"[PLUGIN ERROR] {self.name} v{self.version} | "
            f"attempt={attempt} | {error}"
        )
        traceback.print_exc()

    # =========================
    # ⚙️ CONFIG ACCESS
    # =========================
    def get_config(self, key, default=None):
        return self.config.get(key, default)

    # =========================
    # 🔎 DEBUG
    # =========================
    def __repr__(self):
        return (
            f"<Plugin {self.name} v{self.version} "
            f"(priority={self.priority}, enabled={self.enabled})>"
        )