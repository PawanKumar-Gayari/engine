from copy import deepcopy
import time

from apps.generator.generator import generate_article
from apps.generator.humanizer import Humanizer
from apps.generator.model_router import ModelRouter

from apps.plugins.base.registry import registry
from apps.plugins.seo.seo_plugin import load_seo_plugins


class Pipeline:
    """
    🚀 ULTRA PIPELINE v5 (AI + SELF OPTIMIZING)

    New:
    - adaptive retry strategy
    - smarter scoring
    - execution intelligence
    - better context sharing
    """

    def __init__(self, state):
        self.state = state
        self.max_attempts = 3
        self.history = []
        self.start_time = None

        self.router = ModelRouter()
        self.humanizer = Humanizer()

        # 🔥 load once
        load_seo_plugins()

    # =========================
    # 🚀 MAIN RUNNER
    # =========================
    def run(self):

        self.start_time = time.time()

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

            # 🔥 best tracking
            if score > best_score:
                best_score = score
                best_article = deepcopy(article)

            # 🔥 early stop (AI decision)
            if score >= 85:
                self.state.log("✅ High quality achieved")
                break

            # 🔥 adaptive retry
            if attempt < self.max_attempts:
                article = self._rewrite(article, score, attempt)

        # =========================
        # 🎯 FINALIZE
        # =========================
        self.state.article = best_article or article
        self.state.score = best_score

        self.apply_plugins()
        self.final_score()

        self.state.history = self.history
        self.state.execution_time = round(time.time() - self.start_time, 2)

        return self.state.article, self._summary()

    # =========================
    # 🧠 GENERATE
    # =========================
    def _generate(self):

        self.state.log("🧠 Generating article")

        model_info = self.router.get_model("draft")

        article = generate_article(
            self.state.keyword,
            model=model_info
        )

        # 🔥 humanization
        try:
            article["content"] = self.humanizer.humanize(
                article.get("content", "")
            )
        except Exception as e:
            self.state.log(f"❌ Humanizer error: {e}")

        return article

    # =========================
    # 🔍 VERIFY (SMARTER)
    # =========================
    def _verify(self, article):

        content = article.get("content", "")
        title = article.get("title", "")
        keyword = self.state.keyword.lower()

        score = 0

        # 🔥 content quality
        length = len(content)
        if length > 2000:
            score += 40
        elif length > 1200:
            score += 30
        elif length > 800:
            score += 20
        else:
            score += 10

        # 🔥 keyword relevance
        if keyword in content.lower():
            score += 20

        if keyword in title.lower():
            score += 10

        # 🔥 structure signals
        if "<h2>" in content.lower():
            score += 10

        if "<ul>" in content.lower():
            score += 10

        # 🔥 readability
        if content.count(".") > 20:
            score += 10

        # 🔥 sections
        if "introduction" in content.lower():
            score += 5

        if "conclusion" in content.lower():
            score += 5

        # 🔥 diversity bonus
        if "<table>" in content.lower():
            score += 5

        self.state.log(f"📊 Score: {score}")

        return min(score, 100)

    # =========================
    # 🔁 REWRITE (ADAPTIVE)
    # =========================
    def _rewrite(self, article, score, attempt):

        self.state.log("🔁 AI Rewrite")

        model_info = self.router.get_model("rewrite")

        improved = generate_article(
            self.state.keyword,
            model=model_info,
            base_content=article.get("content", "")
        )

        # 🔥 fallback
        if not improved or "content" not in improved:
            self.state.log("⚠️ Rewrite fallback")
            return article

        return improved

    # =========================
    # 🔥 SEO PLUGINS
    # =========================
    def apply_plugins(self):

        self.state.log("⚙️ Running SEO plugins")

        context = {
            "keyword": self.state.keyword,
            "score": self.state.score,
            "history": self.history,
            "attempts": len(self.history)
        }

        try:
            article, metrics, summary = registry.run_all(
                self.state.article,
                keyword=self.state.keyword,
                intent=self.state.intent,
                context=context,
            )

            # 🔥 final human polish
            article["content"] = self.humanizer.humanize(
                article.get("content", "")
            )

            self.state.article = article
            self.state.plugin_metrics = metrics
            self.state.plugin_summary = summary

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

    # =========================
    # 📊 SUMMARY
    # =========================
    def _summary(self):

        return {
            "attempts": len(self.history),
            "best_score": self.state.score,
            "final_score": self.state.final_score,
            "execution_time": self.state.execution_time,
        }