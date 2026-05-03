import re
import random
from datetime import datetime
from apps.plugins.base.base_plugin import BasePlugin


class TitlePlugin(BasePlugin):
    """
    🚀 AI TITLE ENGINE v5 (A/B + CTR + Competitor Inspired)

    Features:
    - A/B title generation
    - CTR prediction scoring
    - competitor pattern simulation
    - intent-aware title styles
    """

    name = "seo_title"
    priority = 5
    phase = "core"

    MAX_LENGTH = 65

    POWER_WORDS = ["Best", "Latest", "Ultimate", "Complete", "Updated"]
    NUMBER_WORDS = ["Top 5", "Top 10", "7 Proven", "5 Best"]
    STOPWORDS = {"the", "a", "an", "and", "of", "for", "in"}

    CURRENT_YEAR = str(datetime.now().year)

    # =========================
    # 🚀 MAIN
    # =========================
    def run(self, article, keyword="", intent="", context=None):

        context = context or {}

        if isinstance(article, str):
            article = {"content": article}

        keyword = keyword or context.get("keyword") or article.get("title", "")
        keyword = self._clean_keyword(keyword)

        if not keyword:
            return article

        # =========================
        # 🔥 A/B TITLE GENERATION
        # =========================
        titles = self._generate_variants(keyword, intent)

        # =========================
        # 📊 CTR PREDICTION
        # =========================
        scored_titles = [(t, self._predict_ctr(t, keyword)) for t in titles]

        # best title select
        best_title, best_score = max(scored_titles, key=lambda x: x[1])

        article["title"] = best_title
        article["title_score"] = best_score

        # 🔥 store variants (future A/B testing)
        article["title_variants"] = [
            {"title": t, "score": s} for t, s in scored_titles
        ]

        return article

    # =========================
    # 🔥 VARIANT GENERATOR
    # =========================
    def _generate_variants(self, keyword, intent):

        year = self.CURRENT_YEAR
        variants = []

        # style 1: standard SEO
        variants.append(f"{keyword} {year} | Complete Guide & Details")

        # style 2: listicle (high CTR)
        variants.append(f"Top 10 {keyword} {year} | Best Tips & Insights")

        # style 3: question (CTR boost)
        variants.append(f"What is {keyword}? {year} Guide Explained")

        # style 4: power word
        variants.append(f"{random.choice(self.POWER_WORDS)} {keyword} {year} Guide")

        # style 5: intent specific
        if intent == "career":
            variants.append(f"{keyword} {year} Notification | Apply, Salary, Eligibility")

        elif intent == "guide":
            variants.append(f"{keyword} Step-by-Step Guide {year}")

        elif intent == "commercial":
            variants.append(f"Best {keyword} {year} | Top Picks & Reviews")

        return list(set(variants))  # remove duplicates

    # =========================
    # 📊 CTR PREDICTOR
    # =========================
    def _predict_ctr(self, title, keyword):

        score = 0
        text = title.lower()

        # keyword front load
        if text.startswith(keyword.lower()):
            score += 25

        # keyword presence
        if keyword.lower() in text:
            score += 20

        # power words
        if any(p.lower() in text for p in self.POWER_WORDS):
            score += 15

        # numbers boost CTR
        if any(n.lower() in text for n in self.NUMBER_WORDS):
            score += 15

        # question titles
        if "what" in text or "how" in text:
            score += 10

        # optimal length
        if 40 <= len(title) <= 65:
            score += 15

        return min(score, 100)

    # =========================
    # 🧹 CLEAN KEYWORD
    # =========================
    def _clean_keyword(self, keyword):
        keyword = re.sub(r"[^a-zA-Z0-9\s]", "", keyword)
        return keyword.strip().title()