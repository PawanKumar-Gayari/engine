import time
import traceback

from apps.generator.ai_client import generate_openai_content
from apps.plugins.base.registry import registry
from apps.plugins.seo.seo_plugin import load_seo_plugins
from apps.engine.orchestrator import run_pipeline


class SystemHealthCheck:
    """
    🚀 FULL SYSTEM HEALTH CHECK ENGINE
    """

    def __init__(self):
        self.results = {}

    # =========================
    # 🔍 AI CHECK
    # =========================
    def check_ai(self):
        try:
            res = generate_openai_content("test keyword")

            if isinstance(res, dict) and "content" in res:
                self.results["ai"] = "healthy"
            else:
                self.results["ai"] = "failed"

        except Exception as e:
            self.results["ai"] = f"error: {str(e)}"

    # =========================
    # 🔍 PLUGIN CHECK
    # =========================
    def check_plugins(self):
        try:
            load_seo_plugins()

            article = {"content": "test content"}

            result, metrics, summary = registry.run_all(
                article,
                keyword="test keyword",
                intent="guide"
            )

            if "title" in result and "meta_description" in result:
                self.results["plugins"] = "healthy"
            else:
                self.results["plugins"] = "failed"

        except Exception as e:
            self.results["plugins"] = f"error: {str(e)}"

    # =========================
    # 🔍 PIPELINE CHECK
    # =========================
    def check_pipeline(self):
        try:
            res = run_pipeline("test keyword")

            if res.get("status") == "success":
                self.results["pipeline"] = "healthy"
            else:
                self.results["pipeline"] = "failed"

        except Exception as e:
            self.results["pipeline"] = f"error: {str(e)}"

    # =========================
    # 🔍 SCORER CHECK
    # =========================
    def check_scorer(self):
        try:
            article = {
                "content": "<h2>Intro</h2> test content about keyword",
                "title": "Test Keyword Guide",
                "meta_description": "test meta"
            }

            result, _, _ = registry.run_all(
                article,
                keyword="test keyword",
                intent="guide"
            )

            if "seo_score" in result:
                self.results["seo_scorer"] = "healthy"
            else:
                self.results["seo_scorer"] = "failed"

        except Exception as e:
            self.results["seo_scorer"] = f"error: {str(e)}"

    # =========================
    # 🚀 RUN ALL
    # =========================
    def run_all(self):
        start = time.time()

        self.check_ai()
        self.check_plugins()
        self.check_scorer()
        self.check_pipeline()

        duration = round(time.time() - start, 3)

        self.results["total_time"] = duration

        return self.results


# =========================
# 🔥 QUICK FUNCTION
# =========================
def run_health_check():
    checker = SystemHealthCheck()
    return checker.run_all()