import re
import random
from datetime import datetime
from apps.plugins.base.base_plugin import BasePlugin


class MetaPlugin(BasePlugin):
    """
    🚀 SMART META ENGINE v4 (AI + CTR + Context Aware)

    Upgrades:
    - context-aware keyword detection
    - stable CTA (intent based)
    - improved cleaning (no over-removal)
    - better scoring logic
    - string + dict safe
    """

    name = "seo_meta"
    priority = 6
    phase = "core"

    MAX_LENGTH = 155

    POWER_PHRASES = {
        "default": ["Check now", "Explore now"],
        "informational": ["Learn more", "Full guide inside"],
        "commercial": ["Best deals", "Top choices"],
        "career": ["Apply now", "Check eligibility"]
    }

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

        context = context or {}

        # =========================
        # 📦 HANDLE STRING / DICT
        # =========================
        if isinstance(article, str):
            article = {"content": article}

        # =========================
        # 🧠 KEYWORD DETECTION
        # =========================
        keyword = keyword or context.get("keyword") or article.get("title", "")
        keyword = self._clean_keyword(keyword)

        if not keyword:
            return article

        # =========================
        # 🔥 BUILD META
        # =========================
        meta = self._build_meta(keyword, intent)

        # =========================
        # 🔄 VARIATION
        # =========================
        meta = self._add_variation(meta)

        # =========================
        # 🎯 CTA (intent aware)
        # =========================
        meta = self._inject_cta(meta, intent)

        # =========================
        # 🧹 CLEAN
        # =========================
        meta = self._clean_text(meta)

        # =========================
        # ✂️ TRIM
        # =========================
        meta = self._trim(meta)

        # =========================
        # 📊 SCORE
        # =========================
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

        elif intent == "commercial":
            return f"{keyword}: best options, features, pricing and buying guide."

        return f"{keyword} {year}: benefits, usage, features and complete information."

    # =========================
    # 🔄 VARIATION
    # =========================
    def _add_variation(self, meta):

        variation = random.choice(self.VARIATIONS)

        if variation not in meta:
            meta += f" {variation}."

        return meta

    # =========================
    # 🎯 CTA (INTENT BASED)
    # =========================
    def _inject_cta(self, meta, intent):

        cta_list = self.POWER_PHRASES.get(intent, self.POWER_PHRASES["default"])
        cta = random.choice(cta_list)

        if cta.lower() not in meta.lower():
            meta += f" {cta}."

        return meta

    # =========================
    # 🧹 CLEAN TEXT (SAFE)
    # =========================
    def _clean_text(self, text):

        text = re.sub(r"\s+", " ", text)

        # ❌ remove aggressive dedupe (SEO damage करता है)
        text = re.sub(r"\s+\.", ".", text)

        return text.strip()

    # =========================
    # ✂️ TRIM
    # =========================
    def _trim(self, text):

        if len(text) <= self.MAX_LENGTH:
            return text

        return text[:self.MAX_LENGTH].rsplit(" ", 1)[0] + "..."

    # =========================
    # 📊 SMART SCORING
    # =========================
    def _score(self, meta, keyword):

        score = 0
        text = meta.lower()

        # keyword position
        if text.startswith(keyword):
            score += 30
        elif keyword in text:
            score += 20

        # length
        if 120 <= len(meta) <= 160:
            score += 25

        # CTA presence
        if any(p.lower() in text for v in self.POWER_PHRASES.values() for p in v):
            score += 15

        # variation
        if any(v in text for v in self.VARIATIONS):
            score += 10

        # readability
        if "." in meta:
            score += 10

        # penalty
        if text.count(keyword) > 2:
            score -= 10

        return max(0, min(score, 100))