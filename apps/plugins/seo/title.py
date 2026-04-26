import re
import random
from datetime import datetime
from apps.plugins.base.base_plugin import BasePlugin


class TitlePlugin(BasePlugin):
    """
    🚀 ULTIMATE SEO TITLE ENGINE (AI + CTR + Ranking)

    Features:
    - keyword front-loading (SEO boost)
    - dynamic year injection
    - power + number CTR system
    - duplicate + stopword cleanup
    - smart capitalization
    - title scoring system
    - A/B variant support (future ready)
    - over-optimization control
    """

    name = "seo_title"
    priority = 5
    phase = "core"

    MAX_LENGTH = 65

    POWER_WORDS = [
        "Best", "Latest", "Ultimate", "Complete", "Updated"
    ]

    NUMBER_WORDS = [
        "Top 5", "Top 10", "5 Best", "7 Proven"
    ]

    STOPWORDS = {
        "the", "a", "an", "and", "of", "for", "in"
    }

    CURRENT_YEAR = str(datetime.now().year)

    # =========================
    # 🚀 MAIN
    # =========================
    def run(self, article, keyword="", intent="", context=None):

        keyword = keyword.strip()

        if not keyword:
            return article  # 🔒 safety

        # 🔹 clean keyword
        keyword = self._clean_keyword(keyword)

        # 🔹 build base title
        title = self._build_title(keyword, intent)

        # 🔹 inject CTR boosters
        title = self._inject_power(title)

        # 🔹 clean duplicates
        title = self._remove_duplicates(title)

        # 🔹 capitalization
        title = self._capitalize_title(title)

        # 🔹 trim length
        title = self._trim_title(title)

        # 🔹 score title
        score = self._score_title(title, keyword)

        # 🔹 store score (future analytics)
        article["title_score"] = score
        article["title"] = title

        return article

    # =========================
    # 🧹 KEYWORD CLEAN
    # =========================
    def _clean_keyword(self, keyword):

        keyword = re.sub(r"[^a-zA-Z0-9\s]", "", keyword)
        return keyword.strip().title()

    # =========================
    # 🧠 TITLE BUILDER (SEO FIRST)
    # =========================
    def _build_title(self, keyword, intent):

        year = self.CURRENT_YEAR

        # 🔥 keyword always at front (SEO boost)
        if intent == "career":
            return f"{keyword} {year} Notification | Eligibility, Salary, Apply Online"

        elif intent == "education":
            return f"{keyword} {year} | Syllabus, Exam Pattern, Preparation Tips"

        elif intent == "guide":
            return f"{keyword} Guide {year} | Step-by-Step Process"

        return f"{keyword} {year} | Complete Guide, Details"

    # =========================
    # 🔥 POWER + NUMBER INJECTION
    # =========================
    def _inject_power(self, title):

        power = random.choice(self.POWER_WORDS)
        number = random.choice(self.NUMBER_WORDS)

        # avoid over-optimization
        if power.lower() not in title.lower():
            title = f"{power} {title}"

        if random.random() > 0.6:
            title = f"{number} {title}"

        return title

    # =========================
    # 🔁 DUPLICATE REMOVE
    # =========================
    def _remove_duplicates(self, title):

        words = title.split()
        seen = set()
        result = []

        for w in words:
            lw = w.lower()

            if lw not in seen or lw not in self.STOPWORDS:
                result.append(w)
                seen.add(lw)

        return " ".join(result)

    # =========================
    # 🔤 SMART CAPITALIZATION
    # =========================
    def _capitalize_title(self, title):

        words = title.split()

        return " ".join(
            w.capitalize() if w.lower() not in self.STOPWORDS else w
            for w in words
        )

    # =========================
    # ✂️ LENGTH CONTROL
    # =========================
    def _trim_title(self, title):

        if len(title) <= self.MAX_LENGTH:
            return title

        return title[:self.MAX_LENGTH].rsplit(" ", 1)[0]

    # =========================
    # 📊 TITLE SCORING ENGINE
    # =========================
    def _score_title(self, title, keyword):

        score = 0
        text = title.lower()

        # 🔹 keyword presence
        if keyword.lower() in text:
            score += 30

        # 🔹 optimal length
        if 40 <= len(title) <= 65:
            score += 20

        # 🔹 power words
        if any(p.lower() in text for p in self.POWER_WORDS):
            score += 15

        # 🔹 numbers
        if any(n.lower() in text for n in self.NUMBER_WORDS):
            score += 15

        # 🔹 readability (simple heuristic)
        if "|" in title:
            score += 10

        return min(score, 100)