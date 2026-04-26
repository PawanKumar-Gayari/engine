from copy import deepcopy
import time

from apps.generator.generator import generate_article
from apps.generator.humanizer import Humanizer
from apps.generator.model_router import ModelRouter

from apps.plugins.base.registry import registry
from apps.plugins.seo.seo_plugin import load_seo_plugins


class Pipeline:
    """
    🚀 ULTRA PIPELINE v4 (MULTI-MODEL + HUMANIZED AI)

    Features:
    - multi-model orchestration
    - humanization layer
    - best version selection
    - adaptive rewrite
    - SEO plugin integration
    - performance tracking
    """

    def __init__(self, state):
        self.state = state
        self.max_attempts = 3
        self.history = []
        self.start_time = None

        # 🔥 core engines
        self.router = ModelRouter()
        self.humanizer = Humanizer()

    # =========================
    # 🚀 MAIN RUNNER
    # =========================
    def run(self):

        self.start_time = time.time()

        load_seo_plugins()

        best_article = None
        best_score = 0

        for attempt in range(1, self.max_attempts + 1):

            self.state.log(f"🚀 Attempt {attempt}")

            article = self._generate()

            score = self._verify(article)

            self.history.append({
                "attempt": attempt,
                "score": score
            })

            if score > best_score:
                best_score = score
                best_article = deepcopy(article)

            if score >= 85:
                self.state.log("✅ High quality achieved")
                break

            if attempt < self.max_attempts:
                article = self._rewrite(article, score)

        # 🔥 final best content
        self.state.article = best_article or article
        self.state.score = best_score

        # 🔥 SEO
        self.apply_plugins()

        # 🔥 final scoring
        self.final_score()

        # 🔥 stats
        self.state.history = self.history
        self.state.execution_time = round(time.time() - self.start_time, 2)

        return self.state

    # =========================
    # 🧠 GENERATE (MULTI MODEL)
    # =========================
    def _generate(self):

        self.state.log("🧠 Generating article (multi-model)")

        model_info = self.router.get_model("draft")

        article = generate_article(
            self.state.keyword,
            model=model_info
        )

        # 🔥 HUMANIZATION
        try:
            article["content"] = self.humanizer.humanize(
                article.get("content", "")
            )
            self.state.log("✨ Humanized content")
        except Exception as e:
            self.state.log(f"❌ Humanizer error: {e}")

        return article

    # =========================
    # 🔍 VERIFY
    # =========================
    def _verify(self, article):

        content = article.get("content", "")
        title = article.get("title", "")
        keyword = self.state.keyword.lower()

        score = 0

        if len(content) > 1800:
            score += 35
        elif len(content) > 1000:
            score += 25
        else:
            score += 10

        if keyword in content.lower():
            score += 20

        if keyword in title.lower():
            score += 10

        if "<h2>" in content.lower():
            score += 10

        if "<ul>" in content.lower():
            score += 10

        if content.count(".") > 15:
            score += 10

        if "introduction" in content.lower():
            score += 5

        if "conclusion" in content.lower():
            score += 5

        if "<table>" in content.lower():
            score += 5

        self.state.log(f"📊 Score: {score}")

        return score

    # =========================
    # 🔁 REWRITE (AI BASED)
    # =========================
    def _rewrite(self, article, score):

        self.state.log("🔁 AI Rewrite triggered")

        model_info = self.router.get_model("rewrite")

        improved = generate_article(
            self.state.keyword,
            model=model_info,
            base_content=article.get("content", "")
        )

        # fallback if failed
        if not improved or "content" not in improved:
            self.state.log("⚠️ Rewrite fallback used")
            improved = article

        return improved

    # =========================
    # 🔥 SEO PLUGINS
    # =========================
    def apply_plugins(self):

        self.state.log("⚙️ Running SEO plugins")

        context = {
            "keyword": self.state.keyword,
            "score": self.state.score,
            "history": self.history
        }

        try:
            article, metrics, summary = registry.run_all(
                self.state.article,
                keyword=self.state.keyword,
                intent=self.state.intent,
                context=context,
            )

            # 🔥 FINAL HUMAN TOUCH
            article["content"] = self.humanizer.humanize(
                article.get("content", "")
            )

            self.state.article = article
            self.state.plugin_metrics = metrics
            self.state.plugin_summary = summary

            self.state.log("✅ Plugins + Final Humanization")

        except Exception as e:
            self.state.log(f"❌ Plugin error: {e}")

    # =========================
    # 🧠 FINAL SCORE
    # =========================
    def final_score(self):

        base = self.state.score
        meta = self.state.article.get("meta_score", 0)
        seo = self.state.article.get("seo_score", 0)

        final = int((base * 0.5) + (meta * 0.3) + (seo * 0.2))

        self.state.final_score = min(final, 100)

        self.state.log(f"🏁 Final Score: {self.state.final_score}")