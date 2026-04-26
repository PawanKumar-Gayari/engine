import re
import random
from datetime import datetime
from apps.plugins.base.base_plugin import BasePlugin


class MetaPlugin(BasePlugin):
    """
    🚀 ULTRA PRO META ENGINE v3 (SEO + CTR + AI Optimized)

    Features:
    - keyword front loading
    - semantic variation (natural feel)
    - intent-aware templates
    - CTR optimized CTA placement
    - dynamic year injection
    - A/B variation ready
    - anti-spam / over-optimization control
    - advanced scoring (Google-like signals)
    """

    name = "seo_meta"
    priority = 6
    phase = "core"

    MAX_LENGTH = 155

    POWER_PHRASES = [
        "Check now",
        "Don't miss",
        "Latest update",
        "Full details inside",
        "Explore now"
    ]

    VARIATIONS = [
        "complete details",
        "full information",
        "important updates",
        "key insights"
    ]

    CURRENT_YEAR = str(datetime.now().year)

    # =========================
    # 🚀 MAIN
    # =========================
    def run(self, article, keyword="", intent="", context=None):

        keyword = keyword.strip() or article.get("title", "")

        if not keyword:
            return article

        keyword = self._clean_keyword(keyword)

        # 🔹 base meta
        meta = self._build_meta(keyword, intent)

        # 🔹 semantic variation
        meta = self._add_variation(meta)

        # 🔹 CTA injection
        meta = self._inject_cta(meta)

        # 🔹 cleanup
        meta = self._clean_text(meta)

        # 🔹 length control
        meta = self._trim(meta)

        # 🔹 scoring
        score = self._score(meta, keyword)

        article["meta_description"] = meta
        article["meta_score"] = score

        return article

    # =========================
    # 🧹 CLEAN KEYWORD
    # =========================
    def _clean_keyword(self, keyword):
        keyword = re.sub(r"[^a-zA-Z0-9\s]", "", keyword)
        return keyword.strip().lower()

    # =========================
    # 🧠 META BUILDER
    # =========================
    def _build_meta(self, keyword, intent):

        year = self.CURRENT_YEAR

        if intent == "career":
            return f"{keyword} {year}: eligibility, salary, selection process and apply steps explained."

        elif intent == "education":
            return f"{keyword} {year}: syllabus, exam pattern, important topics and preparation strategy."

        elif intent == "guide":
            return f"{keyword}: step-by-step guide, practical tips and real examples."

        return f"{keyword} {year}: benefits, usage, features and complete information."

    # =========================
    # 🔄 SEMANTIC VARIATION
    # =========================
    def _add_variation(self, meta):

        variation = random.choice(self.VARIATIONS)

        if variation not in meta:
            meta = f"{meta} {variation}."

        return meta

    # =========================
    # 🔥 CTA INJECTION
    # =========================
    def _inject_cta(self, meta):

        cta = random.choice(self.POWER_PHRASES)

        # place CTA at end (natural CTR)
        if cta.lower() not in meta.lower():
            meta = f"{meta} {cta}."

        return meta

    # =========================
    # 🔁 CLEAN TEXT
    # =========================
    def _clean_text(self, text):

        text = re.sub(r"\s+", " ", text)

        # remove duplicate words (soft)
        words = text.split()
        seen = set()
        result = []

        for w in words:
            lw = w.lower()
            if lw not in seen:
                result.append(w)
                seen.add(lw)

        text = " ".join(result)

        # punctuation fix
        text = re.sub(r"\s+\.", ".", text)

        return text.strip()

    # =========================
    # ✂️ LENGTH CONTROL
    # =========================
    def _trim(self, text):

        if len(text) <= self.MAX_LENGTH:
            return text

        return text[:self.MAX_LENGTH].rsplit(" ", 1)[0] + "..."

    # =========================
    # 📊 SCORING ENGINE
    # =========================
    def _score(self, meta, keyword):

        score = 0
        text = meta.lower()

        # keyword front boost
        if text.startswith(keyword):
            score += 30
        elif keyword in text:
            score += 20

        # length optimization
        if 120 <= len(meta) <= 160:
            score += 25

        # sentence quality
        if meta.count(".") >= 1:
            score += 10

        # CTR phrases
        if any(p.lower() in text for p in self.POWER_PHRASES):
            score += 15

        # semantic richness
        if any(v in text for v in self.VARIATIONS):
            score += 10

        # penalty (spam)
        if text.count(keyword) > 2:
            score -= 10

        return max(0, min(score, 100))